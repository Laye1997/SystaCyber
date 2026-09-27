from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sensibilisation", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PresenceParticipant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("jeton", models.CharField(max_length=40)),
                ("vu_le", models.DateTimeField(auto_now=True)),
                (
                    "seance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="presences",
                        to="sensibilisation.seance",
                    ),
                ),
            ],
            options={
                "verbose_name": "présence participant",
                "verbose_name_plural": "présences participants",
                "unique_together": {("seance", "jeton")},
            },
        ),
    ]
