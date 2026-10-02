import secrets

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from .forms import (
    EmailExerciceForm,
    EvaluationForm,
    JoindreForm,
    NotesSeanceForm,
    OrganisationForm,
    QuestionForm,
    SeanceForm,
    SlideForm,
    choix_formset,
)
from .models import (
    CasPratique,
    Choix,
    EmailExercice,
    EtapeScenario,
    Evaluation,
    Question,
    ReponseAtelier,
    ReponseQuiz,
    Seance,
    Slide,
    VoteLive,
)
from .pdf import attestations_pdf, rapport_pdf
from .services import etat_seance, marquer_presence, question_live, slides_actives, suivi_activite, texte_lecon


def _jeton(request):
    if not request.session.get("jeton"):
        request.session["jeton"] = secrets.token_hex(16)
    return request.session["jeton"]


def _seance_code(code):
    return get_object_or_404(Seance, code=code.upper())


def _premiere_lecon(seance, jeton):
    votes = ReponseAtelier.objects.filter(seance=seance, jeton_participant=jeton).select_related("email").order_by("email__ordre")
    for v in votes:
        if v.echec and not v.a_lu_lecon:
            return v.email
    return None


def healthz(request):
    """Point de contrôle de santé pour l'hébergeur : renvoie 200 sans auth ni base."""
    return JsonResponse({"status": "ok"})


@login_required
def tableau_de_bord(request):
    seances = Seance.objects.select_related("organisation")[:40]
    return render(request, "formateur/tableau.html", {"seances": seances})


@login_required
def organisation_creer(request):
    # ?next=campagne : revenir au formulaire de campagne avec la nouvelle organisation choisie.
    destination = request.GET.get("next") or request.POST.get("next") or ""
    form = OrganisationForm(request.POST or None)
    if form.is_valid():
        org = form.save()
        messages.success(request, f"{org.nom} enregistrée.")
        if destination == "campagne":
            return redirect(f"{reverse('campagne_creer')}?organisation={org.pk}")
        return redirect("tableau_de_bord")
    return render(request, "formateur/organisation_form.html", {"form": form, "next": destination})


@login_required
def seance_creer(request):
    form = SeanceForm(request.POST or None)
    if form.is_valid():
        seance = form.save()
        messages.success(request, f"Séance créée. Code salle : {seance.code}")
        return redirect(seance)
    return render(request, "formateur/seance_form.html", {"form": form})


@login_required
def seance_modifier(request, pk):
    seance = get_object_or_404(Seance.objects.select_related("organisation"), pk=pk)
    form = SeanceForm(request.POST or None, instance=seance)
    if form.is_valid():
        form.save()
        messages.success(request, "Séance mise à jour.")
        return redirect(seance)
    return render(
        request,
        "formateur/seance_form.html",
        {"form": form, "seance": seance, "edition": True},
    )


@login_required
def pack_contenu(request):
    return render(
        request,
        "formateur/pack.html",
        {
            "questions": Question.objects.prefetch_related("choix"),
            "emails": EmailExercice.objects.all(),
            "slides": Slide.objects.select_related("module"),
        },
    )


@login_required
def question_editer(request, pk=None):
    question = get_object_or_404(Question, pk=pk) if pk else Question()
    FormSet = choix_formset(extra=1 if question.pk else 4)
    form = QuestionForm(request.POST or None, instance=question if question.pk else None)
    formset = FormSet(request.POST or None, instance=question)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        question = form.save()
        formset.instance = question
        formset.save()
        messages.success(request, "Question enregistrée.")
        return redirect("pack_contenu")
    return render(
        request,
        "formateur/question_form.html",
        {"form": form, "formset": formset, "question": question if question.pk else None},
    )


@login_required
@require_http_methods(["POST"])
def question_supprimer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    messages.success(request, "Question supprimée.")
    return redirect("pack_contenu")


@login_required
def email_editer(request, pk=None):
    email = get_object_or_404(EmailExercice, pk=pk) if pk else None
    destination = request.GET.get("next") or request.POST.get("next") or ""
    form = EmailExerciceForm(request.POST or None, instance=email)
    if form.is_valid():
        obj = form.save()
        messages.success(request, "Email d'exercice enregistré.")
        if destination == "campagne":
            return redirect(f"{reverse('campagne_creer')}?modele={obj.pk}")
        return redirect("pack_contenu")
    return render(request, "formateur/email_form.html", {"form": form, "email": email, "next": destination})


@login_required
@require_http_methods(["POST"])
def email_supprimer(request, pk):
    from django.db.models import ProtectedError

    email = get_object_or_404(EmailExercice, pk=pk)
    try:
        email.delete()
        messages.success(request, "Email d'exercice supprimé.")
    except ProtectedError:
        messages.error(
            request,
            "Impossible de supprimer cet email : il est utilisé par une ou plusieurs campagnes. "
            "Supprimez d'abord ces campagnes.",
        )
    return redirect("pack_contenu")


@login_required
def slide_editer(request, pk):
    slide = get_object_or_404(Slide.objects.select_related("module"), pk=pk)
    form = SlideForm(request.POST or None, request.FILES or None, instance=slide)
    if form.is_valid():
        form.save()
        messages.success(request, "Slide mise à jour.")
        return redirect("pack_contenu")
    return render(request, "formateur/slide_form.html", {"form": form, "slide": slide})


@login_required
def seance_detail(request, pk):
    seance = get_object_or_404(Seance.objects.select_related("organisation"), pk=pk)
    if request.method == "POST":
        notes = NotesSeanceForm(request.POST, instance=seance)
        if notes.is_valid():
            notes.save()
            messages.success(request, "Notes enregistrées.")
            return redirect(seance)
    else:
        notes = NotesSeanceForm(instance=seance)
    return render(
        request,
        "formateur/seance_detail.html",
        {
            "seance": seance,
            "notes_form": notes,
            "etat": etat_seance(seance),
            "url_rejoindre": request.build_absolute_uri(reverse("joindre")),
            "suivi": suivi_activite(seance),
            "emails": [
                {"objet": seance.personnaliser(e.objet), "piege": e.piege} for e in seance.emails_choisis()
            ],
            "activites": [
                ("quiz_entree", "Quiz d'entrée", seance.quiz_entree_ouvert),
                ("atelier", "Simulation d'emails", seance.atelier_ouvert),
                ("quiz_sortie", "Quiz de sortie", seance.quiz_sortie_ouvert),
                ("evaluation", "Évaluation", seance.evaluation_ouverte),
            ],
            "live_actions": [
                ("live_prev", "← Précédente"),
                ("live_reveal", "Masquer" if seance.live_reponses_revelees else "Révéler"),
                ("live_next", "Suivante →"),
                ("live_quiz", "Terminer"),
            ],
        },
    )


@login_required
def presenter(request, pk):
    seance = get_object_or_404(Seance.objects.select_related("organisation"), pk=pk)
    slides = slides_actives()
    if not slides:
        messages.error(request, "Aucun module chargé. Exécutez : python manage.py charger_pack")
        return redirect(seance)
    index = min(seance.slide_index, len(slides) - 1)
    slide = slides[index]
    corps = seance.personnaliser(slide.corps)
    notes = seance.personnaliser(slide.notes)
    titre = seance.personnaliser(slide.titre)
    surtitre = seance.personnaliser(slide.surtitre)
    cas = []
    if "Que faites-vous" in slide.titre:
        cas = [
            {
                "lettre": c.lettre,
                "metier": c.metier,
                "situation": seance.personnaliser(c.situation),
                "reponse": seance.personnaliser(c.reponse),
            }
            for c in CasPratique.objects.all()
        ]
    etapes = []
    if slide.type == "scenario":
        etapes = [
            {
                "heure": e.heure,
                "evenement": seance.personnaliser(e.evenement),
                "bonne_reaction": seance.personnaliser(e.bonne_reaction),
            }
            for e in EtapeScenario.objects.all()
        ]
    emails = []
    if slide.type == "atelier":
        emails = [
            {
                "ordre": e.ordre,
                "nom": seance.personnaliser(e.expediteur_nom),
                "objet": seance.personnaliser(e.objet),
                "piege": e.piege,
            }
            for e in seance.emails_choisis()
        ]
    return render(
        request,
        "formateur/presenter.html",
        {
            "seance": seance,
            "slide": slide,
            "titre": titre,
            "surtitre": surtitre,
            "corps": corps,
            "notes": notes,
            "index": index,
            "total": len(slides),
            "etat": etat_seance(seance),
            "cas": cas,
            "etapes": etapes,
            "emails": emails,
        },
    )


@login_required
@require_POST
def seance_action(request, pk):
    seance = get_object_or_404(Seance, pk=pk)
    action = request.POST.get("action")
    slides = slides_actives()
    n = len(slides)
    if action == "next" and n:
        seance.slide_index = min(seance.slide_index + 1, n - 1)
    elif action == "prev" and n:
        seance.slide_index = max(seance.slide_index - 1, 0)
    elif action == "goto":
        try:
            seance.slide_index = max(0, min(int(request.POST.get("index", 0)), max(n - 1, 0)))
        except ValueError:
            return HttpResponseBadRequest()
    elif action == "quiz_entree":
        seance.quiz_entree_ouvert = not seance.quiz_entree_ouvert
        if seance.quiz_entree_ouvert:
            seance.quiz_sortie_ouvert = False
            seance.atelier_ouvert = False
            seance.live_quiz_ouvert = False
    elif action == "quiz_sortie":
        seance.quiz_sortie_ouvert = not seance.quiz_sortie_ouvert
        if seance.quiz_sortie_ouvert:
            seance.quiz_entree_ouvert = False
            seance.atelier_ouvert = False
            seance.live_quiz_ouvert = False
    elif action == "atelier":
        seance.atelier_ouvert = not seance.atelier_ouvert
        if seance.atelier_ouvert:
            seance.quiz_entree_ouvert = False
            seance.quiz_sortie_ouvert = False
            seance.live_quiz_ouvert = False
    elif action == "evaluation":
        seance.evaluation_ouverte = not seance.evaluation_ouverte
    elif action == "live_quiz":
        seance.live_quiz_ouvert = not seance.live_quiz_ouvert
        if seance.live_quiz_ouvert:
            seance.quiz_entree_ouvert = False
            seance.quiz_sortie_ouvert = False
            seance.atelier_ouvert = False
            seance.live_question_index = 0
            seance.live_reponses_revelees = False
            VoteLive.objects.filter(seance=seance).delete()
    elif action == "live_reveal":
        seance.live_reponses_revelees = not seance.live_reponses_revelees
    elif action == "live_next":
        from .services import questions_actives

        nq = max(len(questions_actives()) - 1, 0)
        seance.live_question_index = min(seance.live_question_index + 1, nq)
        seance.live_reponses_revelees = False
    elif action == "live_prev":
        seance.live_question_index = max(seance.live_question_index - 1, 0)
        seance.live_reponses_revelees = False
    else:
        return HttpResponseBadRequest("action inconnue")
    seance.save()
    if request.headers.get("X-Requested-With") == "fetch":
        return JsonResponse(etat_seance(seance))
    nxt = request.POST.get("next")
    if nxt == "presenter":
        return redirect("presenter", pk=seance.pk)
    if nxt == "resultats":
        return redirect("resultats", pk=seance.pk)
    return redirect(seance)


@login_required
def seance_rapport_pdf(request, pk):
    seance = get_object_or_404(Seance.objects.select_related("organisation"), pk=pk)
    return rapport_pdf(seance)


@login_required
def seance_attestations_pdf(request, pk):
    seance = get_object_or_404(Seance.objects.select_related("organisation"), pk=pk)
    return attestations_pdf(seance)


@login_required
def seance_etat_json(request, pk):
    seance = get_object_or_404(Seance, pk=pk)
    return JsonResponse(etat_seance(seance))


@login_required
def resultats(request, pk):
    seance = get_object_or_404(Seance.objects.select_related("organisation"), pk=pk)
    return render(request, "formateur/resultats.html", {"seance": seance, "etat": etat_seance(seance)})


def joindre(request):
    form = JoindreForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data["code"]
        seance = Seance.objects.filter(code=code).first()
        if seance:
            jeton = _jeton(request)
            marquer_presence(seance, jeton, nom=form.cleaned_data["nom"], service=form.cleaned_data.get("service") or "")
            return redirect("participant_salle", code=code)
        form.add_error("code", "Aucune séance avec ce code.")
    return render(request, "participant/joindre.html", {"form": form})


def participant_salle(request, code):
    seance = _seance_code(code)
    marquer_presence(seance, _jeton(request))
    return render(
        request,
        "participant/salle.html",
        {"seance": seance, "etat": etat_seance(seance)},
    )


def participant_etat_json(request, code):
    seance = _seance_code(code)
    jeton = _jeton(request)
    marquer_presence(seance, jeton)
    data = etat_seance(seance)
    data["deja_entree"] = ReponseQuiz.objects.filter(seance=seance, moment="entree", jeton_participant=jeton).exists()
    data["deja_sortie"] = ReponseQuiz.objects.filter(seance=seance, moment="sortie", jeton_participant=jeton).exists()
    data["deja_atelier"] = ReponseAtelier.objects.filter(seance=seance, jeton_participant=jeton).exists()
    data["deja_eval"] = Evaluation.objects.filter(seance=seance, jeton_participant=jeton).exists()
    q = question_live(seance) if seance.live_quiz_ouvert else None
    vote = (
        VoteLive.objects.filter(seance=seance, question=q, jeton_participant=jeton).first()
        if q
        else None
    )
    data["live_choix"] = vote.choix_id if vote else None
    # Le téléphone ne doit connaître ni la bonne réponse ni la répartition avant la révélation.
    live = data["live"]
    if not live["revele"]:
        live["votes"] = [{"id": v["id"], "lettre": v["lettre"], "texte": v["texte"]} for v in live["votes"]]
        if live["question"]:
            live["question"]["explication"] = ""
    for cle in ("entree", "sortie", "phish", "notes"):
        data.pop(cle, None)
    return JsonResponse(data)


@require_POST
def participant_live_vote(request, code):
    seance = _seance_code(code)
    q = question_live(seance)
    if not seance.live_quiz_ouvert or not q or seance.live_reponses_revelees:
        return JsonResponse({"ok": False, "raison": "ferme"}, status=409)
    try:
        choix = Choix.objects.get(pk=int(request.POST.get("choix", 0)), question=q)
    except (ValueError, Choix.DoesNotExist):
        return HttpResponseBadRequest()
    jeton = _jeton(request)
    VoteLive.objects.update_or_create(
        seance=seance, question=q, jeton_participant=jeton, defaults={"choix": choix}
    )
    marquer_presence(seance, jeton)
    return JsonResponse({"ok": True, "choix": choix.id})


def participant_clic(request, code, email_id):
    """Le participant a cliqué le lien de l'email : équivalent du clic dans une campagne Kasap."""
    seance = _seance_code(code)
    if not seance.atelier_ouvert:
        return redirect("participant_salle", code=code)
    email = get_object_or_404(EmailExercice, pk=email_id)
    jeton = _jeton(request)
    vote, _ = ReponseAtelier.objects.get_or_create(
        seance=seance,
        email=email,
        jeton_participant=jeton,
        defaults={"pense_piege": False, "a_ouvert": True},
    )
    vote.a_clique = True
    vote.save(update_fields=["a_clique"])
    if email.piege:
        return redirect("participant_lecon", code=code, email_id=email.id)
    messages.info(request, "Ce lien était légitime : il pointait bien vers un site interne. Bon réflexe de vérifier l'adresse avant.")
    return redirect("participant_atelier", code=code)


def participant_lecon(request, code, email_id):
    seance = _seance_code(code)
    email = get_object_or_404(EmailExercice, pk=email_id)
    jeton = _jeton(request)
    vote = ReponseAtelier.objects.filter(seance=seance, email=email, jeton_participant=jeton).first()
    if request.method == "POST":
        if vote:
            vote.a_lu_lecon = True
            vote.save(update_fields=["a_lu_lecon"])
        suivante = _premiere_lecon(seance, jeton)
        if suivante:
            return redirect("participant_lecon", code=code, email_id=suivante.id)
        messages.success(request, "Merci. Vos réponses sont enregistrées.")
        return redirect("participant_atelier", code=code)
    return render(
        request,
        "participant/lecon.html",
        {
            "seance": seance,
            "email": email,
            "vote": vote,
            "nom": seance.personnaliser(email.expediteur_nom),
            "adresse": seance.personnaliser(email.expediteur_adresse),
            "objet": seance.personnaliser(email.objet),
            "url": seance.personnaliser(email.url_affichee),
            "indices": [seance.personnaliser(i) for i in email.liste_indices()],
            "lecon": texte_lecon(email, seance),
        },
    )


def participant_quiz(request, code, moment):
    if moment not in ("entree", "sortie"):
        return HttpResponseBadRequest()
    seance = _seance_code(code)
    ouvert = seance.quiz_entree_ouvert if moment == "entree" else seance.quiz_sortie_ouvert
    if not ouvert:
        messages.info(request, "Ce quiz n'est pas ouvert pour le moment.")
        return redirect("participant_salle", code=code)
    jeton = _jeton(request)
    existant = ReponseQuiz.objects.filter(seance=seance, moment=moment, jeton_participant=jeton).first()
    questions = list(Question.objects.filter(actif=True).prefetch_related("choix"))
    if request.method == "POST" and not existant:
        score = 0
        reponses = {}
        for q in questions:
            brut = request.POST.get(f"q{q.id}")
            if not brut:
                continue
            try:
                cid = int(brut)
            except ValueError:
                continue
            reponses[str(q.id)] = cid
            if Choix.objects.filter(pk=cid, question=q, correct=True).exists():
                score += 1
        ReponseQuiz.objects.create(
            seance=seance,
            moment=moment,
            jeton_participant=jeton,
            reponses=reponses,
            score=score,
            total=len(questions),
        )
        existant = ReponseQuiz.objects.get(seance=seance, moment=moment, jeton_participant=jeton)
    corriger = bool(existant) and moment == "sortie"
    return render(
        request,
        "participant/quiz.html",
        {
            "seance": seance,
            "moment": moment,
            "questions": questions,
            "existant": existant,
            "corriger": corriger,
            "reponses": existant.reponses if existant else {},
        },
    )


def participant_atelier(request, code):
    seance = _seance_code(code)
    if not seance.atelier_ouvert:
        messages.info(request, "La simulation n'est pas ouverte.")
        return redirect("participant_salle", code=code)
    jeton = _jeton(request)
    emails = seance.emails_choisis()
    votes = {
        v.email_id: v
        for v in ReponseAtelier.objects.filter(seance=seance, jeton_participant=jeton)
    }
    if request.method == "POST":
        for email in emails:
            val = request.POST.get(f"email_{email.id}")
            if val not in ("1", "0"):
                continue
            ReponseAtelier.objects.update_or_create(
                seance=seance,
                email=email,
                jeton_participant=jeton,
                defaults={"pense_piege": val == "1", "a_ouvert": True},
            )
        lecon = _premiere_lecon(seance, jeton)
        if lecon:
            return redirect("participant_lecon", code=code, email_id=lecon.id)
        messages.success(request, "Vos signalements sont enregistrés.")
        return redirect("participant_atelier", code=code)
    personnalises = []
    for e in emails:
        personnalises.append(
            {
                "obj": e,
                "nom": seance.personnaliser(e.expediteur_nom),
                "adresse": seance.personnaliser(e.expediteur_adresse),
                "objet": seance.personnaliser(e.objet),
                "corps": seance.personnaliser(e.corps),
                "url": seance.personnaliser(e.url_affichee),
                "vote": votes.get(e.id),
            }
        )
    termine = len(votes) >= len(emails) > 0
    echecs = sum(1 for v in votes.values() if v.echec)
    n_piege = sum(1 for e in emails if e.piege)
    return render(
        request,
        "participant/atelier.html",
        {
            "seance": seance,
            "emails": personnalises,
            "termine": termine,
            "echecs": echecs,
            "n_piege": n_piege,
        },
    )


def participant_evaluation(request, code):
    seance = _seance_code(code)
    if not seance.evaluation_ouverte:
        messages.info(request, "L'évaluation n'est pas encore ouverte.")
        return redirect("participant_salle", code=code)
    jeton = _jeton(request)
    if Evaluation.objects.filter(seance=seance, jeton_participant=jeton).exists():
        return render(request, "participant/merci.html", {"seance": seance})
    form = EvaluationForm(request.POST or None)
    if form.is_valid():
        notes = {cle: form.cleaned_data[f"note_{cle}"] for cle, _ in Evaluation.CRITERES}
        Evaluation.objects.create(
            seance=seance,
            jeton_participant=jeton,
            notes=notes,
            retient=form.cleaned_data["retient"],
            ameliorer=form.cleaned_data["ameliorer"],
            approfondir=form.cleaned_data["approfondir"],
        )
        return render(request, "participant/merci.html", {"seance": seance})
    return render(request, "participant/evaluation.html", {"seance": seance, "form": form})


# ---------------------------------------------------------------- Campagnes réelles
from django.conf import settings as _settings  # noqa: E402
from django.http import HttpResponse  # noqa: E402
from django.utils import timezone as _tz  # noqa: E402

from .campagnes import CampagneNonAutorisee, envoyer_campagne  # noqa: E402
from .forms import CampagneForm, DestinatairesForm  # noqa: E402
from .models import Campagne, DestinataireCampagne  # noqa: E402


@login_required
def campagnes_liste(request):
    campagnes = Campagne.objects.select_related("organisation", "modele")
    return render(request, "formateur/campagnes.html", {"campagnes": campagnes})


@login_required
def campagne_creer(request):
    initial = {}
    if request.method == "GET":
        for champ in ("organisation", "modele"):
            if request.GET.get(champ):
                initial[champ] = request.GET.get(champ)
    form = CampagneForm(request.POST or None, initial=initial)
    dests_form = DestinatairesForm(request.POST or None)
    dests_form.fields["liste"].required = False
    if form.is_valid() and dests_form.is_valid():
        campagne = form.save()
        ajout = 0
        for d in dests_form.destinataires():
            _, cree = DestinataireCampagne.objects.get_or_create(
                campagne=campagne, email=d["email"], defaults={"nom": d["nom"], "service": d["service"]}
            )
            ajout += int(cree)
        if ajout:
            messages.success(request, f"Campagne créée avec {ajout} destinataire(s).")
        else:
            messages.success(request, "Campagne créée. Ajoutez les destinataires.")
        return redirect(campagne)
    return render(request, "formateur/campagne_form.html", {"form": form, "dests_form": dests_form})


@login_required
def campagne_detail(request, pk):
    campagne = get_object_or_404(Campagne.objects.select_related("organisation", "modele"), pk=pk)
    return render(
        request,
        "formateur/campagne_detail.html",
        {
            "campagne": campagne,
            "form": DestinatairesForm(),
            "stats": campagne.stats(),
            "destinataires": campagne.destinataires.all(),
            "envoi_reel": bool(_settings.EMAIL_HOST),
        },
    )


@login_required
@require_POST
def campagne_destinataires(request, pk):
    campagne = get_object_or_404(Campagne, pk=pk)
    form = DestinatairesForm(request.POST)
    if form.is_valid():
        ajout = 0
        for d in form.destinataires():
            _, cree = DestinataireCampagne.objects.get_or_create(
                campagne=campagne, email=d["email"], defaults={"nom": d["nom"], "service": d["service"]}
            )
            ajout += int(cree)
        messages.success(request, f"{ajout} destinataire(s) ajouté(s).")
    else:
        messages.error(request, "Liste invalide.")
    return redirect(campagne)


@login_required
@require_POST
def campagne_lancer(request, pk):
    campagne = get_object_or_404(Campagne, pk=pk)
    try:
        n = envoyer_campagne(campagne, request)
    except CampagneNonAutorisee as e:
        messages.error(request, str(e))
        return redirect(campagne)
    except Exception as e:
        # Erreur d'envoi (SMTP refusé, expéditeur non validé, etc.) :
        # on affiche le message au lieu de planter en 500.
        messages.error(request, f"Échec de l'envoi : {e}")
        return redirect(campagne)
    messages.success(request, f"{n} email(s) envoyé(s).") if n else messages.info(
        request, "Aucun destinataire à contacter."
    )
    return redirect(campagne)


# --- Traçage (liens publics contenus dans les emails) ---
def campagne_pixel(request, jeton):
    dest = DestinataireCampagne.objects.filter(jeton=jeton).first()
    if dest and not dest.ouvert_le:
        dest.ouvert_le = _tz.now()
        dest.save(update_fields=["ouvert_le"])
    gif = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00"
        b"\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    )
    return HttpResponse(gif, content_type="image/gif")


def campagne_clic(request, jeton):
    """Lien piégé cliqué : on marque le clic et on montre la leçon.

    Si la fausse page est soumise, on note seulement qu'il y a eu une saisie.
    Rien de ce qui est tapé n'est enregistré.
    """
    dest = get_object_or_404(
        DestinataireCampagne.objects.select_related("campagne", "campagne__modele"), jeton=jeton
    )
    now = _tz.now()
    if not dest.clique_le:
        dest.clique_le = now
        if not dest.ouvert_le:
            dest.ouvert_le = now
        dest.save(update_fields=["clique_le", "ouvert_le"])
    if request.method == "POST":
        if not dest.donnees_saisies:
            dest.donnees_saisies = True
            dest.save(update_fields=["donnees_saisies"])
        return redirect("campagne_lecon", jeton=jeton)
    return render(
        request,
        "campagne/faux_portail.html",
        {"dest": dest, "entreprise": dest.campagne.organisation.nom},
    )


def campagne_lecon(request, jeton):
    dest = get_object_or_404(
        DestinataireCampagne.objects.select_related("campagne", "campagne__modele"), jeton=jeton
    )
    if request.method == "POST":
        if not dest.a_lu_lecon:
            dest.a_lu_lecon = True
            dest.save(update_fields=["a_lu_lecon"])
        return render(request, "campagne/merci.html", {"dest": dest})
    campagne = dest.campagne
    email = campagne.modele
    return render(
        request,
        "campagne/lecon.html",
        {
            "dest": dest,
            "entreprise": campagne.organisation.nom,
            "objet": campagne.personnaliser(email.objet, dest),
            "indices": [campagne.personnaliser(i, dest) for i in email.liste_indices()],
            "lecon": campagne.personnaliser(email.page_lecon or "", dest),
            "signalement": campagne.organisation.adresse_signalement,
        },
    )


@login_required
@require_POST
def campagne_supprimer(request, pk):
    campagne = get_object_or_404(Campagne, pk=pk)
    nom = campagne.nom
    campagne.delete()
    messages.success(request, f"Campagne « {nom} » supprimée.")
    return redirect("campagnes_liste")


@login_required
@require_POST
def campagne_signaler(request, pk, dest_pk):
    dest = get_object_or_404(DestinataireCampagne, pk=dest_pk, campagne_id=pk)
    dest.a_signale = not dest.a_signale
    dest.save(update_fields=["a_signale"])
    return redirect("campagne_detail", pk=pk)
