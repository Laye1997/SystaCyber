"""Logique KnowBe4 : baseline, simulation, mesure, benchmark."""

from datetime import timedelta

from django.db.models import Avg, Count
from django.utils import timezone

from .models import Choix, EmailExercice, PresenceParticipant, Question, ReponseAtelier, ReponseQuiz, Slide, VoteLive

PRESENCE_TTL = timedelta(seconds=20)

BENCHMARK_MONDE = 33.2
BENCHMARK_AFRIQUE = 35.9
BENCHMARK_APRES_12_MOIS = 4.2


def slides_actives():
    return list(
        Slide.objects.filter(module__actif=True).select_related("module").order_by("module__ordre", "ordre")
    )


def questions_actives():
    return list(Question.objects.filter(actif=True).prefetch_related("choix").order_by("ordre"))


def stats_quiz(seance, moment):
    qs = ReponseQuiz.objects.filter(seance=seance, moment=moment)
    n = qs.count()
    if not n:
        return {"n": 0, "score_pct": None, "moyenne": None}
    agg = qs.aggregate(m=Avg("score"), t=Avg("total"))
    total = agg["t"] or 0
    moyenne = agg["m"] or 0
    pct = round(100 * moyenne / total, 1) if total else None
    return {"n": n, "score_pct": pct, "moyenne": round(moyenne, 2), "total": round(total, 2)}


def stats_phish_prone(seance):
    emails = seance.emails_choisis()
    emails_piege_ids = [e.id for e in emails if e.piege]
    votes = ReponseAtelier.objects.filter(seance=seance, email_id__in=emails_piege_ids).select_related("email")
    participants = set(votes.values_list("jeton_participant", flat=True))
    if not participants:
        return {
            "n": 0,
            "phish_prone_pct": None,
            "echecs": 0,
            "votes_piege": 0,
            "taux_echec_emails": None,
            "clics": 0,
            "signalements": 0,
        }
    echecs_users = set()
    echecs_votes = 0
    clics = 0
    signalements = 0
    for v in votes:
        if v.pense_piege:
            signalements += 1
        if v.a_clique:
            clics += 1
        if v.echec:
            echecs_users.add(v.jeton_participant)
            echecs_votes += 1
    n = len(participants)
    n_votes = votes.count()
    return {
        "n": n,
        "phish_prone_pct": round(100 * len(echecs_users) / n, 1),
        "echecs": len(echecs_users),
        "votes_piege": n_votes,
        "taux_echec_emails": round(100 * echecs_votes / n_votes, 1) if n_votes else None,
        "clics": clics,
        "signalements": signalements,
    }


def marquer_presence(seance, jeton, nom="", service=""):
    if not jeton:
        return None
    obj, created = PresenceParticipant.objects.get_or_create(seance=seance, jeton=jeton)
    champs = ["vu_le"]
    if nom and obj.nom != nom:
        obj.nom = nom
        champs.append("nom")
    if service and obj.service != service:
        obj.service = service
        champs.append("service")
    obj.save(update_fields=champs)
    return obj


def compter_connectes(seance):
    seuil = timezone.now() - PRESENCE_TTL
    return PresenceParticipant.objects.filter(seance=seance, vu_le__gte=seuil).count()


def question_live(seance):
    qs = questions_actives()
    if not qs:
        return None
    return qs[min(seance.live_question_index, len(qs) - 1)]


def etat_live(seance):
    q = question_live(seance)
    questions = questions_actives()
    if not q:
        return {
            "live_quiz_ouvert": seance.live_quiz_ouvert,
            "question": None,
            "index": 0,
            "total": 0,
            "revele": seance.live_reponses_revelees,
            "votes": [],
            "total_votes": 0,
        }
    counts = {
        row["choix_id"]: row["n"]
        for row in VoteLive.objects.filter(seance=seance, question=q).values("choix_id").annotate(n=Count("id"))
    }
    total = sum(counts.values())
    votes = []
    for c in q.choix.all():
        n = counts.get(c.id, 0)
        votes.append(
            {
                "id": c.id,
                "lettre": c.lettre,
                "texte": c.texte,
                "correct": c.correct,
                "n": n,
                "pct": round(100 * n / total) if total else 0,
            }
        )
    return {
        "live_quiz_ouvert": seance.live_quiz_ouvert,
        "question": {"id": q.id, "texte": q.texte, "explication": q.explication},
        "index": seance.live_question_index,
        "total": len(questions),
        "revele": seance.live_reponses_revelees,
        "votes": votes,
        "total_votes": total,
    }


def suivi_activite(seance):
    presences = list(PresenceParticipant.objects.filter(seance=seance).order_by("nom", "jeton"))
    jetons = [p.jeton for p in presences]
    entree = set(
        ReponseQuiz.objects.filter(seance=seance, moment="entree", jeton_participant__in=jetons).values_list(
            "jeton_participant", flat=True
        )
    )
    sortie = set(
        ReponseQuiz.objects.filter(seance=seance, moment="sortie", jeton_participant__in=jetons).values_list(
            "jeton_participant", flat=True
        )
    )
    atelier = set(
        ReponseAtelier.objects.filter(seance=seance, jeton_participant__in=jetons).values_list("jeton_participant", flat=True)
    )
    return [
        {
            "nom": p.nom or "Anonyme",
            "service": p.service,
            "jeton": p.jeton,
            "connecte": p.vu_le >= timezone.now() - PRESENCE_TTL,
            "entree": p.jeton in entree,
            "atelier": p.jeton in atelier,
            "sortie": p.jeton in sortie,
        }
        for p in presences
    ]


def texte_lecon(email, seance):
    brut = (email.page_lecon or "").strip()
    if not brut:
        items = "".join(f"<li>{seance.personnaliser(i)}</li>" for i in email.liste_indices())
        brut = (
            "<p>Cet email était un <strong>piège</strong>. Un vrai message de ce type "
            "aurait pu compromettre un compte ou une donnée de {entreprise}.</p>"
            f"<p>Points à retenir :</p><ul>{items}</ul>"
            "<p>Réflexe : ne jamais communiquer un mot de passe, un code ou un RIB "
            "depuis un lien reçu par email. Vérifier par un autre canal "
            "({contact_it} / {signalement}).</p>"
        )
    return seance.personnaliser(brut)


def actions_recommandees(etat):
    actions = []
    phish = etat["phish"].get("phish_prone_pct")
    if phish is None:
        actions.append("Relancer une simulation d'emails dès que le groupe a terminé l'atelier, pour mesurer un taux d'exposition.")
    elif phish >= 30:
        actions.append("Taux d'exposition élevé : programmer une nouvelle simulation dans 30 jours, avec des modèles locaux (colis, paie, paiement mobile).")
    elif phish >= 15:
        actions.append("Conserver une simulation trimestrielle et rappeler le canal de signalement interne à chaque équipe.")
    else:
        actions.append("Bon réflexe collectif : maintenir une simulation semestrielle pour éviter que le taux ne remonte.")

    delta = etat.get("delta_connaissance")
    if delta is None:
        actions.append("Faire passer le quiz de sortie en fin de journée pour chiffrer la progression des connaissances.")
    elif delta < 5:
        actions.append("Progression limitée : insister en atelier sur 2–3 pièges manqués (expéditeur, lien, urgence) plutôt que d'ajouter du contenu.")
    else:
        actions.append("Capitaliser la progression : envoyer un mémo d'une page (réflexes + n° interne) dans la semaine.")

    actions.append("Nommer un relais par service pour signaler un email suspect, et afficher {signalement} / le contact informatique sur l'intranet.")
    return actions[:3]


def etat_seance(seance):
    entree = stats_quiz(seance, "entree")
    sortie = stats_quiz(seance, "sortie")
    phish = stats_phish_prone(seance)
    delta = None
    if entree["score_pct"] is not None and sortie["score_pct"] is not None:
        delta = round(sortie["score_pct"] - entree["score_pct"], 1)
    live = etat_live(seance)
    return {
        "quiz_entree_ouvert": seance.quiz_entree_ouvert,
        "quiz_sortie_ouvert": seance.quiz_sortie_ouvert,
        "atelier_ouvert": seance.atelier_ouvert,
        "evaluation_ouverte": seance.evaluation_ouverte,
        "live_quiz_ouvert": seance.live_quiz_ouvert,
        "live_reponses_revelees": seance.live_reponses_revelees,
        "slide_index": seance.slide_index,
        "code": seance.code,
        "entree": entree,
        "sortie": sortie,
        "phish": phish,
        "delta_connaissance": delta,
        "evaluations": seance.evaluations.count(),
        "participants_connectes": compter_connectes(seance),
        "participants_prevus": seance.participants_prevus,
        "benchmark_monde": BENCHMARK_MONDE,
        "benchmark_afrique": BENCHMARK_AFRIQUE,
        "benchmark_cible": BENCHMARK_APRES_12_MOIS,
        "live": live,
        "quiz_entree_recus": entree["n"],
        "quiz_sortie_recus": sortie["n"],
    }
