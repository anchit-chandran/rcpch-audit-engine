# Generated by Django 4.0.5 on 2022-07-02 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epilepsy12', '0003_alter_desscribe_epileptic_generalised_onset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desscribe',
            name='syndrome',
            field=models.IntegerField(blank=True, choices=[(27, 'CDKL5-DEE'), (16, 'Childhood absence epilepsy'), (5, 'Childhood occipital visual epilepsy'), (34, 'DEE or EE with spike-and-wave activation in sleep'), (23, 'Dravet syndrome'), (20, 'Early infantile DEE'), (21, 'Epilepsy of infancy with migrating focal seizures'), (11, 'Epilepsy with auditory features'), (15, 'Epilepsy with eyelid myoclonia'), (19, 'Epilepsy with generalized tonic–clonic seizures alone'), (14, 'Epilepsy with myoclonic absences'), (32, 'Epilepsy with myoclonic–atonic seizures'), (39, 'Epilepsy with reading-induced seizures'), (24, 'Etiology-specific DEEs'), (10, 'Familial focal epilepsy with variable foci'), (8, 'Familial mesial temporal lobe epilepsy'), (35, 'Febrile infection-related epilepsy syndrome'), (29, 'GLUT1DS-DEE'), (31, 'Gelastic seizures with HH'), (12, 'Genetic epilepsy with febrile seizures plus'), (36, 'Hemiconvulsion–hemiplegia–epilepsy'), (22, 'Infantile epileptic spasms syndrome'), (17, 'Juvenile absence epilepsy'), (18, 'Juvenile myoclonic epilepsy'), (25, 'KCNQ2-DEE'), (33, 'Lennox–Gastaut syndrome'), (7, 'Mesial temporal lobe epilepsy with hippocampal sclerosis'), (13, 'Myoclonic epilepsy in infancy'), (28, 'PCDH19 clustering epilepsy'), (6, 'Photosensitive occipital lobe epilepsy'), (38, 'Progressive myoclonus epilepsies'), (26, 'Pyridoxine-dependent and pyridox(am)ine 5′ phosphate deficiency DEE'), (37, 'Rasmussen syndrome'), (1, 'Self-limited (familial) infantile epilepsy'), (0, 'Self-limited (familial) neonatal epilepsy'), (4, 'Self-limited epilepsy with autonomic seizures'), (3, 'Self-limited epilepsy with centrotemporal spikes'), (2, 'Self-limited familial neonatal-infantile epilepsy'), (9, 'Sleep-related hypermotor (hyperkinetic) epilepsy'), (30, 'Sturge–Weber syndrome')], default=None, null=True, verbose_name='Is there an identifiable epilepsy syndrome?'),
        ),
    ]