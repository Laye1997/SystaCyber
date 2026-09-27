from django.core.management.base import BaseCommand
from django.db.models import Max

from sensibilisation.modeles_locaux import MODELES_LOCAUX
from sensibilisation.models import EmailExercice, Slide
from sensibilisation.pack_contenu import EMAILS, MODULES


class Command(BaseCommand):
    help = (
        "Ajoute la bibliothèque de modèles locaux et les vidéos sans effacer le contenu existant "
        "(contrairement à charger_pack). Peut être relancée sans créer de doublons."
    )

    def handle(self, *args, **options):
        # Emails du pack générique : compléter catégorie et lien si vides.
        maj = 0
        for e in EMAILS:
            for obj in EmailExercice.objects.filter(objet=e["objet"]):
                champs = []
                for cle in ("categorie", "url_affichee"):
                    if e.get(cle) and not getattr(obj, cle):
                        setattr(obj, cle, e[cle])
                        champs.append(cle)
                if champs:
                    obj.save(update_fields=champs)
                    maj += 1

        # Modèles locaux : ajoutés à la bibliothèque, hors pack par défaut.
        ajoutes = 0
        ordre = EmailExercice.objects.aggregate(m=Max("ordre"))["m"] or 0
        for modele in MODELES_LOCAUX:
            if EmailExercice.objects.filter(objet=modele["objet"]).exists():
                continue
            ordre += 1
            EmailExercice.objects.create(ordre=ordre, actif=False, **modele)
            ajoutes += 1

        # Vidéos déclarées dans le pack.
        videos = 0
        for mod in MODULES:
            for sl in mod["slides"]:
                if sl.get("video_youtube"):
                    videos += Slide.objects.filter(titre=sl["titre"], type=sl.get("type", "contenu"), video_youtube="").update(
                        video_youtube=sl["video_youtube"]
                    )

        self.stdout.write(
            self.style.SUCCESS(f"{ajoutes} modèle(s) ajouté(s), {maj} email(s) complété(s), {videos} vidéo(s) posée(s).")
        )
