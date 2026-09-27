from datetime import date

from django.core.management.base import BaseCommand

from sensibilisation.models import CasPratique, Choix, EmailExercice, EtapeScenario, Module, Organisation, Question, Seance, Slide
from sensibilisation.modeles_locaux import MODELES_LOCAUX
from sensibilisation.pack_contenu import CAS, EMAILS, MODULES, QUESTIONS, SCENARIO


class Command(BaseCommand):
    help = "Charge le pack pédagogique générique (modules, quiz, simulation emails)."

    def add_arguments(self, parser):
        parser.add_argument("--demo", action="store_true", help="Crée une organisation et une séance de démonstration.")

    def handle(self, *args, **options):
        Slide.objects.all().delete()
        Module.objects.all().delete()
        Question.objects.all().delete()
        EmailExercice.objects.all().delete()
        CasPratique.objects.all().delete()
        EtapeScenario.objects.all().delete()

        for i, mod in enumerate(MODULES):
            module = Module.objects.create(
                ordre=i,
                numero=mod.get("numero", ""),
                titre=mod["titre"],
                horaire=mod.get("horaire", ""),
                duree_minutes=mod.get("duree", 30),
            )
            for j, sl in enumerate(mod["slides"]):
                Slide.objects.create(module=module, ordre=j, **sl)

        for i, q in enumerate(QUESTIONS, start=1):
            question = Question.objects.create(ordre=i, texte=q["texte"], explication=q["explication"])
            for lettre, texte, correct in q["choix"]:
                Choix.objects.create(question=question, lettre=lettre, texte=texte, correct=correct)

        for i, e in enumerate(EMAILS, start=1):
            EmailExercice.objects.create(ordre=i, **e)
        for i, e in enumerate(MODELES_LOCAUX, start=len(EMAILS) + 1):
            EmailExercice.objects.create(ordre=i, actif=False, **e)

        for c in CAS:
            CasPratique.objects.create(**c)

        for i, s in enumerate(SCENARIO, start=1):
            EtapeScenario.objects.create(ordre=i, **s)

        n_slides = Slide.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Pack chargé : {Module.objects.count()} modules, {n_slides} slides, {Question.objects.count()} questions, {EmailExercice.objects.count()} emails."))

        if options.get("demo"):
            org, _ = Organisation.objects.get_or_create(
                nom="BCI Banque",
                defaults={
                    "secteur": "banque",
                    "domaine_email": "bci-banque.sn",
                    "contact_it": "3012",
                    "adresse_signalement": "signalement@bci-banque.sn",
                },
            )
            seance, created = Seance.objects.get_or_create(
                organisation=org,
                date=date.today(),
                groupe="Groupe A",
                defaults={"formateur": "Abdoulaye Diaw", "lieu": "Dakar", "participants_prevus": 30},
            )
            self.stdout.write(self.style.SUCCESS(f"Séance démo {'créée' if created else 'existante'} — code {seance.code}"))
