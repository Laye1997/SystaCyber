from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import EmailExercice, Organisation, ReponseAtelier, Seance
from .services import stats_phish_prone


class PhishProneTests(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(nom="Demo", domaine_email="demo.sn")
        self.seance = Seance.objects.create(organisation=self.org, date="2026-09-26", formateur="Test")
        self.piege = EmailExercice.objects.create(
            ordre=1,
            expediteur_nom="X",
            expediteur_adresse="a@b.c",
            objet="piège",
            corps="...",
            piege=True,
            indices="x",
        )
        EmailExercice.objects.create(
            ordre=2,
            expediteur_nom="Y",
            expediteur_adresse="y@demo.sn",
            objet="ok",
            corps="...",
            piege=False,
            indices="y",
        )

    def test_phish_prone_click_equivalent(self):
        ReponseAtelier.objects.create(seance=self.seance, email=self.piege, jeton_participant="a", pense_piege=False)
        ReponseAtelier.objects.create(seance=self.seance, email=self.piege, jeton_participant="b", pense_piege=True)
        stats = stats_phish_prone(self.seance)
        self.assertEqual(stats["n"], 2)
        self.assertEqual(stats["phish_prone_pct"], 50.0)

    def test_joindre_code(self):
        r = self.client.post(reverse("joindre"), {"code": self.seance.code})
        self.assertEqual(r.status_code, 302)
        self.assertIn(self.seance.code, r["Location"])


class FormateurTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("formateur", password="secret12")
        self.org = Organisation.objects.create(nom="Demo")
        self.seance = Seance.objects.create(organisation=self.org, date="2026-09-26", formateur="Test")

    def test_tableau_exige_connexion(self):
        r = self.client.get(reverse("tableau_de_bord"))
        self.assertEqual(r.status_code, 302)

    def test_ouvrir_quiz(self):
        self.client.login(username="formateur", password="secret12")
        r = self.client.post(reverse("seance_action", args=[self.seance.pk]), {"action": "quiz_entree"})
        self.assertEqual(r.status_code, 302)
        self.seance.refresh_from_db()
        self.assertTrue(self.seance.quiz_entree_ouvert)

    def test_compteur_participants_connectes(self):
        from .services import compter_connectes

        self.assertEqual(compter_connectes(self.seance), 0)
        participant = self.client_class()
        participant.post(reverse("joindre"), {"code": self.seance.code})
        r = participant.get(reverse("participant_etat_json", args=[self.seance.code]))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(compter_connectes(self.seance), 1)

        self.client.login(username="formateur", password="secret12")
        etat = self.client.get(reverse("seance_etat_json", args=[self.seance.pk]))
        self.assertEqual(etat.status_code, 200)
        self.assertEqual(etat.json()["participants_connectes"], 1)

    def test_modifier_seance(self):
        self.client.login(username="formateur", password="secret12")
        r = self.client.post(
            reverse("seance_modifier", args=[self.seance.pk]),
            {
                "organisation": self.org.pk,
                "date": "2026-10-01",
                "groupe": "Groupe B",
                "lieu": "Dakar",
                "formateur": "Diaw",
                "participants_prevus": 18,
            },
        )
        self.assertEqual(r.status_code, 302)
        self.seance.refresh_from_db()
        self.assertEqual(self.seance.participants_prevus, 18)
        self.assertEqual(self.seance.groupe, "Groupe B")
        self.assertEqual(str(self.seance.date), "2026-10-01")

    def test_pack_accessible(self):
        self.client.login(username="formateur", password="secret12")
        r = self.client.get(reverse("pack_contenu"))
        self.assertEqual(r.status_code, 200)


class QuizLiveTests(TestCase):
    def setUp(self):
        from .models import Choix, Question

        self.user = User.objects.create_user("formateur", password="secret12")
        self.org = Organisation.objects.create(nom="Demo")
        self.seance = Seance.objects.create(organisation=self.org, date="2026-09-26", formateur="Test")
        self.q = Question.objects.create(ordre=1, texte="Q1 ?", explication="Parce que.")
        self.bon = Choix.objects.create(question=self.q, lettre="A", texte="Bon", correct=True)
        self.faux = Choix.objects.create(question=self.q, lettre="B", texte="Faux")
        self.client.login(username="formateur", password="secret12")
        self.client.post(reverse("seance_action", args=[self.seance.pk]), {"action": "live_quiz"})
        self.participant = self.client_class()
        self.participant.post(reverse("joindre"), {"code": self.seance.code})

    def test_vote_puis_revelation(self):
        url_vote = reverse("participant_live_vote", args=[self.seance.code])
        self.assertEqual(self.participant.post(url_vote, {"choix": self.faux.pk}).status_code, 200)
        # Changer d'avis remplace le vote.
        self.assertEqual(self.participant.post(url_vote, {"choix": self.bon.pk}).status_code, 200)

        etat = self.participant.get(reverse("participant_etat_json", args=[self.seance.code])).json()
        self.assertEqual(etat["live_choix"], self.bon.pk)
        self.assertNotIn("correct", etat["live"]["votes"][0], "la bonne réponse ne doit pas fuiter avant révélation")
        self.assertEqual(etat["live"]["question"]["explication"], "")

        formateur = self.client.get(reverse("seance_etat_json", args=[self.seance.pk])).json()
        self.assertEqual(formateur["live"]["total_votes"], 1)

        self.client.post(reverse("seance_action", args=[self.seance.pk]), {"action": "live_reveal"})
        etat = self.participant.get(reverse("participant_etat_json", args=[self.seance.code])).json()
        self.assertTrue(etat["live"]["votes"][0]["correct"])
        # Plus de vote après révélation.
        self.assertEqual(self.participant.post(url_vote, {"choix": self.faux.pk}).status_code, 409)

    def test_choix_d_une_autre_question_refuse(self):
        from .models import Choix, Question

        autre = Question.objects.create(ordre=2, texte="Q2 ?")
        c = Choix.objects.create(question=autre, lettre="A", texte="x")
        r = self.participant.post(reverse("participant_live_vote", args=[self.seance.code]), {"choix": c.pk})
        self.assertEqual(r.status_code, 400)


class SimulationLeconTests(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(nom="Demo", domaine_email="demo.sn")
        self.seance = Seance.objects.create(
            organisation=self.org, date="2026-09-26", formateur="Test", atelier_ouvert=True
        )
        self.piege = EmailExercice.objects.create(
            ordre=1, expediteur_nom="Wave", expediteur_adresse="x@wave-transfert.com", objet="Transfert",
            corps="...", piege=True, indices="Argent inattendu", url_affichee="http://wave-transfert.com",
        )
        self.legit = EmailExercice.objects.create(
            ordre=2, expediteur_nom="RH", expediteur_adresse="rh@demo.sn", objet="Paie", corps="...",
            piege=False, indices="interne", url_affichee="https://intranet.demo.sn",
        )
        self.client.post(reverse("joindre"), {"code": self.seance.code, "nom": "Awa", "service": "Crédit"})

    def test_clic_sur_piege_mene_a_la_lecon(self):
        r = self.client.get(reverse("participant_clic", args=[self.seance.code, self.piege.pk]))
        self.assertRedirects(r, reverse("participant_lecon", args=[self.seance.code, self.piege.pk]))
        vote = ReponseAtelier.objects.get(seance=self.seance, email=self.piege)
        self.assertTrue(vote.a_clique)
        self.assertTrue(vote.echec)
        self.assertEqual(stats_phish_prone(self.seance)["phish_prone_pct"], 100.0)

        page = self.client.get(reverse("participant_lecon", args=[self.seance.code, self.piege.pk]))
        self.assertContains(page, "Argent inattendu")
        self.client.post(reverse("participant_lecon", args=[self.seance.code, self.piege.pk]))
        vote.refresh_from_db()
        self.assertTrue(vote.a_lu_lecon)

    def test_clic_sur_lien_legitime_sans_lecon(self):
        r = self.client.get(reverse("participant_clic", args=[self.seance.code, self.legit.pk]))
        self.assertRedirects(r, reverse("participant_atelier", args=[self.seance.code]))

    def test_classer_piege_legitime_affiche_la_lecon(self):
        r = self.client.post(
            reverse("participant_atelier", args=[self.seance.code]),
            {f"email_{self.piege.pk}": "0", f"email_{self.legit.pk}": "0"},
        )
        self.assertRedirects(r, reverse("participant_lecon", args=[self.seance.code, self.piege.pk]))

    def test_selection_de_modeles_hors_pack(self):
        self.piege.actif = False
        self.piege.save()
        self.assertEqual(self.seance.emails_choisis(), [self.legit])
        self.seance.emails_simulation.set([self.piege])
        self.assertEqual(self.seance.emails_choisis(), [self.piege])


class PdfTests(TestCase):
    def setUp(self):
        User.objects.create_user("formateur", password="secret12")
        self.org = Organisation.objects.create(nom="Demo")
        self.seance = Seance.objects.create(organisation=self.org, date="2026-09-26", formateur="Test")
        participant = self.client_class()
        participant.post(reverse("joindre"), {"code": self.seance.code, "nom": "Moussa <b>", "service": "IT"})
        self.client.login(username="formateur", password="secret12")

    def test_rapport_et_attestations(self):
        for nom in ("seance_rapport_pdf", "seance_attestations_pdf"):
            r = self.client.get(reverse(nom, args=[self.seance.pk]))
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r["Content-Type"], "application/pdf")
            self.assertTrue(r.content.startswith(b"%PDF"))

    def test_pages_formateur(self):
        from .models import Module, Slide

        module = Module.objects.create(titre="M")
        Slide.objects.create(module=module, type="section", titre="Phishing", video_youtube="FOA8qcDE50o")
        page = self.client.get(reverse("presenter", args=[self.seance.pk]))
        self.assertContains(page, "youtube-nocookie.com/embed/FOA8qcDE50o")
        self.client.post(reverse("seance_action", args=[self.seance.pk]), {"action": "live_quiz"})
        self.assertContains(self.client.get(reverse("presenter", args=[self.seance.pk])), "Quiz en direct")
        for nom in ("seance_detail", "presenter", "seance_modifier"):
            self.assertEqual(self.client.get(reverse(nom, args=[self.seance.pk])).status_code, 200, nom)


class VideoLocaleTests(TestCase):
    def test_envoi_mp4_et_lecture_dans_la_slide(self):
        import shutil
        import tempfile

        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.test import override_settings

        from .models import Module, Slide

        dossier = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, dossier, True)
        with override_settings(MEDIA_ROOT=dossier):
            User.objects.create_user("formateur", password="secret12")
            self.client.login(username="formateur", password="secret12")
            seance = Seance.objects.create(organisation=Organisation.objects.create(nom="Demo"), date="2026-09-26", formateur="T")
            slide = Slide.objects.create(module=Module.objects.create(titre="M"), type="section", titre="Phishing", video_youtube="FOA8qcDE50o")
            data = {"ordre": 0, "type": "section", "titre": "Phishing", "video_youtube": "FOA8qcDE50o",
                    "video_fichier": SimpleUploadedFile("fbf.mp4", b"ftypmp42", content_type="video/mp4")}
            r = self.client.post(reverse("slide_editer", args=[slide.pk]), data)
            self.assertEqual(r.status_code, 302)
            slide.refresh_from_db()
            self.assertTrue(slide.video_fichier.name.startswith("videos/fbf"))

            page = self.client.get(reverse("presenter", args=[seance.pk]))
            self.assertContains(page, "<video src=\"/media/videos/fbf")
            self.assertNotContains(page, "youtube-nocookie")
            self.assertEqual(self.client.get(slide.video_fichier.url).status_code, 200)

            data["video_fichier"] = SimpleUploadedFile("virus.exe", b"MZ", content_type="application/octet-stream")
            r = self.client.post(reverse("slide_editer", args=[slide.pk]), data)
            self.assertEqual(r.status_code, 200)
            self.assertContains(r, "mp4")
