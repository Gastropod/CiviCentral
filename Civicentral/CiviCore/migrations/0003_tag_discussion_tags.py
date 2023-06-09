# Generated by Django 4.2 on 2023-04-22 02:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CiviCore", "0002_remove_vote_element_id_remove_vote_vote_type_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=60)),
                ("description", models.TextField(max_length=180)),
            ],
        ),
        migrations.AddField(
            model_name="discussion",
            name="tags",
            field=models.ManyToManyField(blank=True, to="CiviCore.tag"),
        ),
    ]
