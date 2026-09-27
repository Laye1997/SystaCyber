from django.core.management.base import BaseCommand
from django.db import transaction

from sensibilisation.models import Module, Seance, Slide
from sensibilisation.pack_contenu import MODULES


class Command(BaseCommand):
    help = (
        "Recharge uniquement les modules et slides du pack (programme sur deux jours). "
        "Questions, emails, séances et résultats sont conservés, ainsi que les vidéos locales déjà envoyées."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        videos = {s.titre: s.video_fichier.name for s in Slide.objects.exclude(video_fichier="")}
        Slide.objects.all().delete()
        Module.objects.all().delete()
        for i, mod in enumerate(MODULES):
            module = Module.objects.create(
                ordre=i,
                numero=mod.get("numero", ""),
                titre=mod["titre"],
                horaire=mod.get("horaire", ""),
                duree_minutes=mod.get("duree", 30),
            )
            for j, sl in enumerate(mod["slides"]):
                slide = Slide(module=module, ordre=j, **sl)
                if sl["titre"] in videos:
                    slide.video_fichier.name = videos[sl["titre"]]
                slide.save()
        Seance.objects.update(slide_index=0)
        self.stdout.write(
            self.style.SUCCESS(f"Programme chargé : {Module.objects.count()} modules, {Slide.objects.count()} slides.")
        )
