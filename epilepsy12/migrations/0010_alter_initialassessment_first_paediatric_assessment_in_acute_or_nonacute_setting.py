# Generated by Django 4.1.2 on 2022-10-17 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0009_alter_case_ethnicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialassessment',
            name='first_paediatric_assessment_in_acute_or_nonacute_setting',
            field=models.IntegerField(choices=[(1, 'Acute'), (2, 'Non-acute'), (3, "Don't know")], default=None, help_text={'label': 'Is the first paediatric assessment in an acute or nonacute setting?', 'reference': 'This is a reference.'}, null=True),
        ),
    ]
