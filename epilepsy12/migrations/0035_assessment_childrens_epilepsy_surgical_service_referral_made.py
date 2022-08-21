# Generated by Django 4.0.4 on 2022-08-13 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0034_alter_assessment_childrens_epilepsy_surgical_service_referral_criteria_met_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='childrens_epilepsy_surgical_service_referral_made',
            field=models.BooleanField(default=None, null=True, verbose_name="Has a referral to a children's epilepsy surgery service been made?"),
        ),
    ]