# Generated by Django 3.1.4 on 2021-12-04 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_date', models.DateField(auto_now=True, verbose_name='Date de mise à jour')),
                ('name', models.CharField(max_length=150, verbose_name='Nom')),
                ('race', models.CharField(blank=True, max_length=150, verbose_name='Race')),
                ('food', models.CharField(blank=True, max_length=300, verbose_name='Alimentation')),
                ('activities', models.CharField(blank=True, max_length=300, verbose_name='Activité(s)')),
                ('living_place', models.CharField(blank=True, max_length=150, verbose_name='Lieu de vie')),
                ('origin', models.CharField(choices=[('REFUGE', 'Refuge'), ('ELEVAGE', 'Elevage'), ('PARTICULIER', 'Particulier'), ('ANIMALERIE', 'Animalerie'), ('DIVAGATION', 'Divagation')], max_length=50, verbose_name="Lieu d'adoption")),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Date de naissance')),
                ('adoption_age', models.CharField(blank=True, max_length=50, verbose_name="Age d'adoption")),
                ('date_arrivee', models.DateField(blank=True, null=True, verbose_name='Date de prise en charge')),
                ('sex', models.CharField(choices=[('F', 'Femelle'), ('M', 'Mâle')], max_length=30, verbose_name='Sexe')),
                ('type', models.CharField(choices=[('CHIEN', 'Chien'), ('CHAT', 'Chat'), ('CHEVAL', 'Cheval'), ('LAPIN', 'Lapin'), ('COCHON_INDE', "Cochon d'inde"), ('CHEVRE', 'Chèvre'), ('MOUTON', 'Mouton'), ('REPTILE', 'Reptile')], max_length=30, verbose_name='Espèce')),
                ('sterilised', models.CharField(choices=[('OUI', 'Oui'), ('NON', 'Non')], max_length=3, verbose_name='Stérilisé(e)')),
                ('identification', models.CharField(blank=True, max_length=150, verbose_name="Numéro d'identification")),
                ('meadow_address', models.CharField(blank=True, max_length=300, verbose_name='Adresse du pré')),
            ],
        ),
    ]