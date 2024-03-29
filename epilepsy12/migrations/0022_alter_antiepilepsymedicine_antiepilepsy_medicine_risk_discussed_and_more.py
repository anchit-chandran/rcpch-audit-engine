# Generated by Django 4.1.2 on 2022-10-23 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0021_alter_antiepilepsymedicine_antiepilepsy_medicine_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antiepilepsymedicine',
            name='antiepilepsy_medicine_risk_discussed',
            field=models.BooleanField(blank=True, default=None, help_text={'label': 'Medication risks discussed?', 'reference': 'Have the risks related to the antiseizure medicine been discussed with the child/young person and their family?'}, null=True),
        ),
        migrations.AlterField(
            model_name='antiepilepsymedicine',
            name='antiepilepsy_medicine_snomed_code',
            field=models.CharField(blank=True, default=None, help_text={'label': 'Antiseizure/rescue medicine SNOMED-CT code', 'reference': 'Antiseizure medicine SNOMED-CT code'}, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='antiepilepsymedicine',
            name='antiepilepsy_medicine_snomed_preferred_name',
            field=models.CharField(blank=True, default=None, help_text={'label': 'Antiseizure/rescue medicine SNOMED-CT preferred name', 'reference': 'Antiseizure medicine SNOMED-CT preferred name'}, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='antiepilepsymedicine',
            name='antiepilepsy_medicine_start_date',
            field=models.DateField(blank=True, default=None, help_text={'label': 'Medicine start date', 'reference': 'Antiepilepsy medicine start date'}, null=True),
        ),
        migrations.AlterField(
            model_name='antiepilepsymedicine',
            name='antiepilepsy_medicine_stop_date',
            field=models.DateField(blank=True, default=None, help_text={'label': 'Medicine discontinued date', 'reference': 'Antiseizure medicine discontinued date'}, null=True),
        ),
        migrations.AlterField(
            model_name='antiepilepsymedicine',
            name='antiepilepsy_medicine_type',
            field=models.IntegerField(blank=True, default=None, help_text={'label': 'Medicine name', 'reference': 'Please enter antiseizure medicine name.'}, null=True),
        ),
    ]
