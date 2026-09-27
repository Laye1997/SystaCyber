from django.contrib import admin

from . import models


@admin.register(models.Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("nom", "secteur", "domaine_email", "contact_it")
    search_fields = ("nom",)


class SlideInline(admin.StackedInline):
    model = models.Slide
    extra = 0
    fields = ("ordre", "type", "quiz_moment", "surtitre", "titre", "corps", "notes")


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("ordre", "numero", "titre", "horaire", "duree_minutes", "actif")
    list_editable = ("actif",)
    inlines = [SlideInline]


class ChoixInline(admin.TabularInline):
    model = models.Choix
    extra = 0


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("ordre", "texte", "actif")
    list_editable = ("actif",)
    inlines = [ChoixInline]


@admin.register(models.EmailExercice)
class EmailExerciceAdmin(admin.ModelAdmin):
    list_display = ("ordre", "expediteur_nom", "objet", "piege")


@admin.register(models.CasPratique)
class CasPratiqueAdmin(admin.ModelAdmin):
    list_display = ("lettre", "metier", "situation")


@admin.register(models.EtapeScenario)
class EtapeScenarioAdmin(admin.ModelAdmin):
    list_display = ("ordre", "heure", "evenement")


@admin.register(models.Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ("organisation", "date", "groupe", "formateur", "code")
    list_filter = ("organisation",)
    readonly_fields = ("code",)


@admin.register(models.ReponseAtelier)
class ReponseAtelierAdmin(admin.ModelAdmin):
    list_display = ("seance", "email", "pense_piege", "cree_le")
    list_filter = ("seance", "pense_piege")


@admin.register(models.ReponseQuiz)
class ReponseQuizAdmin(admin.ModelAdmin):
    list_display = ("seance", "moment", "score", "total", "cree_le")
    list_filter = ("seance", "moment")


@admin.register(models.Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("seance", "cree_le")
    list_filter = ("seance",)
