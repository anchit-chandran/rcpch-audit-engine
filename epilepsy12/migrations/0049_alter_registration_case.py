# Generated by Django 4.0.4 on 2022-08-21 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0048_rename_investigation_management_complete_auditprogress_investigation_complete_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='case',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='epilepsy12.case'),
        ),
    ]