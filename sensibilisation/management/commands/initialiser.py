"""Prépare l'application au démarrage (idempotent) : compte admin + contenu.

Utile sur un hébergeur sans shell : la commande est lancée au démarrage du
conteneur. Elle ne fait rien si tout est déjà en place.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from sensibilisation.models import Module


class Command(BaseCommand):
    help = "Crée le compte admin et charge le contenu s'ils n'existent pas encore."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@systalink.com")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Compte superutilisateur '{username}' créé."))
        else:
            self.stdout.write(f"Compte '{username}' déjà présent.")

        if not Module.objects.exists():
            call_command("charger_programme")
        else:
            self.stdout.write("Programme déjà chargé.")

        # Idempotent : n'ajoute que les modèles manquants.
        call_command("charger_modeles")
        self.stdout.write(self.style.SUCCESS("Initialisation terminée."))
