"""Ne garde dans la bibliothèque que les emails de référence (pack + modèles locaux).

Les emails créés pour des campagnes (ou des tests) sont retirés de la
bibliothèque (bibliotheque=False) sans être supprimés.
"""
from django.db import migrations


def nettoyer(apps, schema_editor):
    from sensibilisation.modeles_locaux import MODELES_LOCAUX
    from sensibilisation.pack_contenu import EMAILS

    objets_reference = {e["objet"] for e in EMAILS} | {m["objet"] for m in MODELES_LOCAUX}
    EmailExercice = apps.get_model("sensibilisation", "EmailExercice")
    EmailExercice.objects.filter(bibliotheque=True).exclude(objet__in=objets_reference).update(bibliotheque=False)


def inverse(apps, schema_editor):
    # Pas de retour en arrière automatique : on ne devine pas quels emails remettre.
    pass


class Migration(migrations.Migration):
    dependencies = [("sensibilisation", "0006_email_bibliotheque")]
    operations = [migrations.RunPython(nettoyer, inverse)]
