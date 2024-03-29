# Generated by Django 4.1.5 on 2023-01-28 18:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0052_alter_registration_options_alter_site_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'permissions': [('can_allocate_epilepsy12_lead_centre', 'Can allocate this child to any Epilepsy12 centre.'), ('can_transfer_epilepsy12_lead_centre', 'Can transfer this child to another Epilepsy12 centre.'), ('can_edit_epilepsy12_lead_centre', "Can edit this child's current Epilepsy12 lead centre."), ('can_delete_epilepsy12_lead_centre', 'Can delete Epilepsy12 lead centre.')], 'verbose_name': 'Site', 'verbose_name_plural': 'Sites'},
        ),
        migrations.AlterField(
            model_name='visitactivity',
            name='activity_datetime',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
    ]
