"""Modèles de l'application Systalink CyberSécurité.

Le contenu pédagogique (modules, slides, quiz, emails d'atelier, cas,
scénario) est générique : il contient des jetons comme {entreprise} ou
{domaine} remplacés à l'affichage par les informations du client de la
séance. Un même contenu sert donc pour toutes les entreprises.
"""
import secrets
import string

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


def generer_code():
    alphabet = string.ascii_uppercase.replace("O", "").replace("I", "") + "23456789"
    return "".join(secrets.choice(alphabet) for _ in range(6))


# ---------------------------------------------------------------- Clients
class Organisation(models.Model):
    nom = models.CharField("Nom de l'entreprise", max_length=150)
    secteur = models.CharField("Secteur", max_length=100, blank=True, help_text="Ex. : banque, assurance, industrie")
    domaine_email = models.CharField("Domaine email", max_length=100, blank=True, help_text="Ex. : bci-banque.sn")
    contact_it = models.CharField("Contact informatique (numéro interne)", max_length=100, blank=True)
    adresse_signalement = models.CharField("Adresse pour signaler un email suspect", max_length=150, blank=True)
    contact_client = models.CharField("Contact client (nom, email)", max_length=200, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "organisation cliente"

    def __str__(self):
        return self.nom


# ---------------------------------------------------------------- Contenu
class Module(models.Model):
    ordre = models.PositiveIntegerField(default=0)
    numero = models.CharField("Numéro affiché", max_length=20, blank=True, help_text="Ex. : Module 1 (vide pour ouverture/clôture)")
    titre = models.CharField(max_length=200)
    horaire = models.CharField(max_length=20, blank=True)
    duree_minutes = models.PositiveIntegerField(default=30)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordre"]

    def __str__(self):
        return f"{self.numero} {self.titre}".strip()


class Slide(models.Model):
    TYPES = [
        ("titre", "Titre / couverture"),
        ("section", "Intro de module"),
        ("contenu", "Contenu"),
        ("chiffre", "Chiffre clé"),
        ("activite", "Activité"),
        ("quiz", "Lancement de quiz"),
        ("atelier", "Atelier emails (interactif)"),
        ("scenario", "Scénario d'incident (interactif)"),
    ]
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="slides")
    ordre = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=20, choices=TYPES, default="contenu")
    surtitre = models.CharField(max_length=200, blank=True)
    titre = models.CharField(max_length=250)
    corps = models.TextField(blank=True, help_text="HTML simple. Jetons : {entreprise} {domaine} {contact_it} {signalement} {formateur} {date}")
    notes = models.TextField("Notes du formateur", blank=True)
    quiz_moment = models.CharField(max_length=10, blank=True, choices=[("entree", "Entrée"), ("sortie", "Sortie")])
    video_youtube = models.CharField("ID vidéo YouTube", max_length=20, blank=True, help_text="Ex. : FOA8qcDE50o")
    video_fichier = models.FileField(
        "Vidéo locale (MP4)",
        upload_to="videos/",
        blank=True,
        validators=[FileExtensionValidator(["mp4", "webm"])],
        help_text="Lue sans Internet, prioritaire sur YouTube. Formats : MP4 ou WebM.",
    )

    class Meta:
        ordering = ["module__ordre", "ordre"]

    def __str__(self):
        return self.titre


class Question(models.Model):
    ordre = models.PositiveIntegerField(default=0)
    texte = models.TextField()
    explication = models.TextField("Message à faire passer", blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordre"]

    def __str__(self):
        return f"Q{self.ordre}. {self.texte[:60]}"


class Choix(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choix")
    lettre = models.CharField(max_length=2)
    texte = models.CharField(max_length=300)
    correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["lettre"]
        verbose_name_plural = "choix"

    def __str__(self):
        return f"{self.lettre}. {self.texte}"


class EmailExercice(models.Model):
    ordre = models.PositiveIntegerField(default=0)
    expediteur_nom = models.CharField(max_length=150)
    expediteur_adresse = models.CharField(max_length=200)
    objet = models.CharField(max_length=250)
    corps = models.TextField()
    piege = models.BooleanField("Piégé ?", default=True)
    indices = models.TextField(help_text="Un indice par ligne")
    categorie = models.CharField(max_length=40, blank=True, help_text="Ex. : wave, colis, banque, interne")
    url_affichee = models.CharField("Lien affiché au survol", max_length=250, blank=True)
    page_lecon = models.TextField("Leçon après un clic", blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordre"]
        verbose_name = "email d'exercice"
        verbose_name_plural = "emails d'exercice"

    def __str__(self):
        return f"Email {self.ordre} — {self.objet}"

    def liste_indices(self):
        return [l.strip() for l in self.indices.splitlines() if l.strip()]


class CasPratique(models.Model):
    lettre = models.CharField(max_length=2)
    metier = models.CharField(max_length=80)
    situation = models.TextField()
    reponse = models.TextField("Réponse attendue")

    class Meta:
        ordering = ["lettre"]
        verbose_name = "cas pratique"

    def __str__(self):
        return f"Cas {self.lettre} — {self.metier}"


class EtapeScenario(models.Model):
    ordre = models.PositiveIntegerField(default=0)
    heure = models.CharField(max_length=20)
    evenement = models.TextField()
    bonne_reaction = models.TextField()

    class Meta:
        ordering = ["ordre"]
        verbose_name = "étape du scénario"

    def __str__(self):
        return f"{self.heure} — {self.evenement[:50]}"


# ---------------------------------------------------------------- Séances
class Seance(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT, related_name="seances")
    date = models.DateField()
    groupe = models.CharField(max_length=50, blank=True, help_text="Ex. : Groupe A")
    lieu = models.CharField(max_length=150, blank=True)
    formateur = models.CharField(max_length=150)
    participants_prevus = models.PositiveIntegerField(default=30)
    presents = models.PositiveIntegerField(null=True, blank=True)
    code = models.CharField(max_length=8, unique=True, default=generer_code, editable=False)
    quiz_entree_ouvert = models.BooleanField(default=False)
    quiz_sortie_ouvert = models.BooleanField(default=False)
    evaluation_ouverte = models.BooleanField(default=False)
    notes_formateur = models.TextField("Questions et remarques de la salle", blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    slide_index = models.PositiveIntegerField(default=0)
    atelier_ouvert = models.BooleanField(default=False)
    scenario_ouvert = models.BooleanField(default=False)
    live_quiz_ouvert = models.BooleanField(default=False)
    live_question_index = models.PositiveIntegerField(default=0)
    live_reponses_revelees = models.BooleanField(default=False)
    emails_simulation = models.ManyToManyField(
        EmailExercice,
        blank=True,
        related_name="seances",
        help_text="Vide = tous les emails actifs.",
    )

    class Meta:
        ordering = ["-date", "groupe"]
        verbose_name = "séance"

    def __str__(self):
        return f"{self.organisation} — {self.date:%d/%m/%Y} {self.groupe}".strip()

    def get_absolute_url(self):
        return reverse("seance_detail", args=[self.pk])

    def jetons(self):
        org = self.organisation
        return {
            "{entreprise}": org.nom,
            "{secteur}": org.secteur or "votre organisation",
            "{domaine}": org.domaine_email or "[domaine]",
            "{contact_it}": org.contact_it or "[numéro de l'informatique]",
            "{signalement}": org.adresse_signalement or "[adresse de signalement]",
            "{formateur}": self.formateur,
            "{date}": self.date.strftime("%d/%m/%Y"),
            "{groupe}": self.groupe,
        }

    def personnaliser(self, texte):
        for jeton, valeur in self.jetons().items():
            texte = texte.replace(jeton, valeur)
        return texte

    def emails_choisis(self):
        # Une sélection explicite peut puiser dans toute la bibliothèque ;
        # "actif" définit seulement le pack par défaut.
        selection = self.emails_simulation.all()
        if selection.exists():
            return list(selection.order_by("ordre"))
        return list(EmailExercice.objects.filter(actif=True).order_by("ordre"))


class ReponseAtelier(models.Model):
    """Vote KnowBe4 : le participant classe un email (signaler vs légitime)."""

    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name="reponses_atelier")
    email = models.ForeignKey(EmailExercice, on_delete=models.CASCADE, related_name="votes")
    jeton_participant = models.CharField(max_length=40)
    pense_piege = models.BooleanField("A signalé comme piégé")
    a_ouvert = models.BooleanField(default=False)
    a_clique = models.BooleanField(default=False)
    a_lu_lecon = models.BooleanField(default=False)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("seance", "email", "jeton_participant")]
        verbose_name = "réponse à l'atelier"
        verbose_name_plural = "réponses à l'atelier"

    @property
    def echec(self):
        """Échec : piège classé légitime ou lien ouvert (équivalent du clic KnowBe4 / Kasap)."""
        return self.email.piege and (self.a_clique or not self.pense_piege)


class ReponseQuiz(models.Model):
    MOMENTS = [("entree", "Entrée"), ("sortie", "Sortie")]
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name="reponses_quiz")
    moment = models.CharField(max_length=10, choices=MOMENTS)
    jeton_participant = models.CharField(max_length=40)
    reponses = models.JSONField(default=dict, help_text="{question_id: choix_id}")
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("seance", "moment", "jeton_participant")]
        verbose_name = "réponse au quiz"
        verbose_name_plural = "réponses au quiz"


class Evaluation(models.Model):
    CRITERES = [
        ("utile", "Le contenu est utile pour mon travail quotidien"),
        ("reconnaitre", "Je saurai reconnaître un email suspect"),
        ("reagir", "Je sais quoi faire si je clique sur un lien suspect"),
        ("ateliers", "Les ateliers pratiques m'ont aidé à comprendre"),
        ("formateur", "Le formateur était clair et disponible"),
        ("duree", "La durée de la journée était adaptée"),
        ("recommande", "Je recommanderais cette séance à un collègue"),
    ]
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name="evaluations")
    jeton_participant = models.CharField(max_length=40)
    notes = models.JSONField(default=dict)
    retient = models.TextField("Ce que je retiens", blank=True)
    ameliorer = models.TextField("À améliorer", blank=True)
    approfondir = models.TextField("À approfondir", blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("seance", "jeton_participant")]


class PresenceParticipant(models.Model):
    """Participant actuellement dans la salle (battement de présence)."""

    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name="presences")
    jeton = models.CharField(max_length=40)
    nom = models.CharField(max_length=120, blank=True)
    service = models.CharField(max_length=120, blank=True)
    vu_le = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("seance", "jeton")]
        verbose_name = "présence participant"
        verbose_name_plural = "présences participants"

    def __str__(self):
        return self.nom or self.jeton[:8]


class VoteLive(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name="votes_live")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="votes_live")
    jeton_participant = models.CharField(max_length=40)
    choix = models.ForeignKey(Choix, on_delete=models.CASCADE)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("seance", "question", "jeton_participant")]
        verbose_name = "vote quiz live"
