from django import forms
from django.forms import inlineformset_factory

from .models import Choix, EmailExercice, Evaluation, Organisation, Question, Seance, Slide


class JoindreForm(forms.Form):
    nom = forms.CharField(label="Prénom et nom (facultatif)", max_length=120, required=False, help_text="Uniquement pour l'émargement et l'attestation. Vos réponses restent anonymes.")
    service = forms.CharField(label="Service / équipe", max_length=120, required=False)
    code = forms.CharField(
        label="Code de la séance",
        max_length=8,
        widget=forms.TextInput(attrs={"autocomplete": "off", "autocapitalize": "characters", "placeholder": "ABC123"}),
    )

    def clean_code(self):
        return self.cleaned_data["code"].strip().upper()


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ["nom", "secteur", "domaine_email", "contact_it", "adresse_signalement", "contact_client"]


class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ["organisation", "date", "groupe", "lieu", "formateur", "participants_prevus", "presents", "emails_simulation"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "emails_simulation": forms.CheckboxSelectMultiple,
        }
        labels = {"emails_simulation": "Emails de la simulation"}
        help_texts = {"emails_simulation": "Cochez les modèles à utiliser (6 à 8 conseillés). Rien de coché = le pack par défaut."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].input_formats = ["%Y-%m-%d"]
        self.fields["emails_simulation"].queryset = EmailExercice.objects.order_by("categorie", "ordre")
        self.fields["emails_simulation"].label_from_instance = lambda e: (
            f"{'[' + e.categorie + '] ' if e.categorie else ''}{e.objet}{'  · piège' if e.piege else '  · légitime'}"
        )


class NotesSeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ["presents", "notes_formateur"]
        widgets = {"notes_formateur": forms.Textarea(attrs={"rows": 5})}


class EvaluationForm(forms.Form):
    retient = forms.CharField(label="Ce que je retiens en priorité", required=False, widget=forms.Textarea(attrs={"rows": 2}))
    ameliorer = forms.CharField(label="Ce qui pourrait être amélioré", required=False, widget=forms.Textarea(attrs={"rows": 2}))
    approfondir = forms.CharField(label="Un sujet à approfondir", required=False, widget=forms.Textarea(attrs={"rows": 2}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for cle, libelle in Evaluation.CRITERES:
            self.fields[f"note_{cle}"] = forms.TypedChoiceField(
                label=libelle,
                choices=[(i, str(i)) for i in range(1, 6)],
                coerce=int,
                widget=forms.RadioSelect,
            )
        # critères en premier
        ordre = [f"note_{c}" for c, _ in Evaluation.CRITERES] + ["retient", "ameliorer", "approfondir"]
        self.order_fields(ordre)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["ordre", "texte", "explication", "actif"]
        widgets = {
            "texte": forms.Textarea(attrs={"rows": 3}),
            "explication": forms.Textarea(attrs={"rows": 3}),
        }


class ChoixForm(forms.ModelForm):
    class Meta:
        model = Choix
        fields = ["lettre", "texte", "correct"]


def choix_formset(extra=1):
    return inlineformset_factory(
        Question,
        Choix,
        form=ChoixForm,
        extra=extra,
        can_delete=True,
        min_num=2,
        validate_min=True,
    )


class EmailExerciceForm(forms.ModelForm):
    class Meta:
        model = EmailExercice
        fields = [
            "ordre", "categorie", "expediteur_nom", "expediteur_adresse", "objet", "corps", "url_affichee",
            "piege", "indices", "page_lecon", "actif",
        ]
        labels = {"actif": "Dans le pack par défaut"}
        help_texts = {
            "actif": "Coché : utilisé quand la séance n'a pas de sélection. Décoché : reste dans la bibliothèque.",
            "page_lecon": "HTML simple. Vide = leçon générée à partir des indices.",
        }
        widgets = {
            "corps": forms.Textarea(attrs={"rows": 6}),
            "indices": forms.Textarea(attrs={"rows": 4}),
            "page_lecon": forms.Textarea(attrs={"rows": 5}),
        }


class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ["ordre", "type", "surtitre", "titre", "corps", "notes", "quiz_moment", "video_fichier", "video_youtube"]
        widgets = {
            "corps": forms.Textarea(attrs={"rows": 8}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
