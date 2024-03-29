# Generated by Django 4.1.2 on 2022-10-23 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0020_alter_antiepilepsymedicine_antiepilepsy_medicine_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antiepilepsymedicine',
            name='antiepilepsy_medicine_type',
            field=models.IntegerField(blank=True, choices=[(1, 'ACTH'), (0, 'Acetazolamide'), (2, 'Carbamazepine'), (3, 'Clobazam'), (4, 'Clonazepam'), (28, 'Epidyolex® '), (5, 'Eslicarbazepine acetate'), (6, 'Ethosuximide'), (31, 'Gabapentin'), (7, 'Lacosamide'), (8, 'Lamotrigine'), (9, 'Levetiracetam'), (10, 'Methylprednisolone'), (11, 'Nitrazepam'), (30, 'Other'), (29, 'Other Cannabis-based medicinal product'), (12, 'Oxcarbazepine'), (13, 'Perampanel'), (15, 'Phenobarbital'), (16, 'Phenytoin'), (14, 'Piracetam'), (18, 'Prednisolone'), (17, 'Pregabalin'), (19, 'Primidone'), (20, 'Rufinamide'), (21, 'Sodium valproate'), (22, 'Stiripentol'), (23, 'Sulthiame'), (24, 'Tiagabine'), (25, 'Topiramate'), (26, 'Vigabatrin'), (27, 'Zonisamide')], default=None, help_text={'label': 'Antiseizure medicine name', 'reference': 'Please enter antiseizure medicine name.'}, null=True),
        ),
    ]
