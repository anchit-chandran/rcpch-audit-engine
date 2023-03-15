# Generated by Django 4.1.7 on 2023-03-14 15:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("epilepsy12", "0057_historicalhospitaltrust_country_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="episode",
            name="description",
            field=models.CharField(
                blank=True,
                default="",
                help_text={
                    "label": "What is the episode(s) like and is the description adequate?",
                    "reference": "What is the episode(s) like and is the description adequate?",
                },
                max_length=2000,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalepisode",
            name="description",
            field=models.CharField(
                blank=True,
                default="",
                help_text={
                    "label": "What is the episode(s) like and is the description adequate?",
                    "reference": "What is the episode(s) like and is the description adequate?",
                },
                max_length=2000,
                null=True,
            ),
        ),
    ]