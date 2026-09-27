from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sensibilisation", "0002_presenceparticipant"),
    ]

    operations = [
        migrations.AddField(
            model_name="slide",
            name="video_youtube",
            field=models.CharField(blank=True, help_text="Ex. : FOA8qcDE50o", max_length=20, verbose_name="ID vidéo YouTube"),
        ),
        migrations.AddField(
            model_name="emailexercice",
            name="actif",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="emailexercice",
            name="categorie",
            field=models.CharField(blank=True, help_text="Ex. : wave, colis, banque, interne", max_length=40),
        ),
        migrations.AddField(
            model_name="emailexercice",
            name="page_lecon",
            field=models.TextField(blank=True, verbose_name="Leçon après un clic"),
        ),
        migrations.AddField(
            model_name="emailexercice",
            name="url_affichee",
            field=models.CharField(blank=True, max_length=250, verbose_name="Lien affiché au survol"),
        ),
        migrations.AddField(
            model_name="seance",
            name="live_quiz_ouvert",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="seance",
            name="live_question_index",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="seance",
            name="live_reponses_revelees",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="seance",
            name="emails_simulation",
            field=models.ManyToManyField(blank=True, help_text="Vide = tous les emails actifs.", related_name="seances", to="sensibilisation.emailexercice"),
        ),
        migrations.AddField(
            model_name="reponseatelier",
            name="a_clique",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="reponseatelier",
            name="a_lu_lecon",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="reponseatelier",
            name="a_ouvert",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="presenceparticipant",
            name="nom",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="presenceparticipant",
            name="service",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.CreateModel(
            name="VoteLive",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("jeton_participant", models.CharField(max_length=40)),
                ("cree_le", models.DateTimeField(auto_now_add=True)),
                ("choix", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="sensibilisation.choix")),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="votes_live", to="sensibilisation.question")),
                ("seance", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="votes_live", to="sensibilisation.seance")),
            ],
            options={
                "verbose_name": "vote quiz live",
                "unique_together": {("seance", "question", "jeton_participant")},
            },
        ),
    ]
