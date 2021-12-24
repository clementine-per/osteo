# Generated by Django 3.1.4 on 2021-12-23 10:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


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
                ('living_place', models.CharField(blank=True, max_length=300, verbose_name='Lieu de vie')),
                ('food', models.CharField(blank=True, max_length=300, verbose_name='Alimentation')),
                ('activities', models.CharField(blank=True, max_length=300, verbose_name='Activité(s)')),
                ('origin', models.CharField(choices=[('REFUGE', 'Refuge'), ('ELEVAGE', 'Elevage'), ('PARTICULIER', 'Particulier'), ('ANIMALERIE', 'Animalerie'), ('DIVAGATION', 'Divagation')], max_length=50, verbose_name="Lieu d'adoption")),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Date de naissance')),
                ('adoption_age', models.CharField(blank=True, max_length=50, verbose_name="Age d'adoption")),
                ('sex', models.CharField(choices=[('F', 'Femelle'), ('M', 'Mâle')], max_length=30, verbose_name='Sexe')),
                ('type', models.CharField(choices=[('CHIEN', 'Chien'), ('CHAT', 'Chat'), ('CHEVAL', 'Cheval'), ('LAPIN', 'Lapin'), ('COCHON_INDE', "Cochon d'inde"), ('CHEVRE', 'Chèvre'), ('MOUTON', 'Mouton'), ('REPTILE', 'Reptile')], max_length=30, verbose_name='Espèce')),
                ('sterilised', models.CharField(choices=[('OUI', 'Oui'), ('NON', 'Non')], max_length=3, verbose_name='Stérilisé(e)')),
                ('identification', models.CharField(blank=True, max_length=150, verbose_name="Numéro d'identification")),
                ('meadow_address', models.CharField(blank=True, max_length=300, verbose_name='Adresse du pré')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_consult_date', models.DateField(blank=True, null=True, verbose_name='Date de dernière consultation ostéopathique')),
                ('vaccinated', models.CharField(choices=[('OUI', 'Oui'), ('NON', 'Non')], max_length=3, verbose_name='Vacciné(e)')),
                ('ape_api', models.CharField(choices=[('OUI', 'Oui'), ('NON', 'Non')], max_length=3, verbose_name='Traité(e) APE/API')),
                ('antecedents', models.CharField(blank=True, max_length=300, verbose_name='Antécédents médicaux')),
                ('surgeries', models.CharField(blank=True, max_length=300, verbose_name='Chirurgie(s)')),
                ('locomotor_disorders', models.CharField(blank=True, max_length=300, verbose_name='Troubles locomoteurs')),
                ('past_treatments', models.CharField(blank=True, max_length=300, verbose_name='Traitements passés')),
                ('current_treatments', models.CharField(blank=True, max_length=300, verbose_name='Traitements actuels')),
                ('behaviour', models.CharField(blank=True, max_length=300, verbose_name='Comportement')),
                ('other', models.CharField(blank=True, max_length=300, verbose_name='Autres')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_date', models.DateField(auto_now=True, verbose_name='Date de mise à jour')),
                ('first_name', models.CharField(max_length=30, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=150, verbose_name='Nom')),
                ('email', models.EmailField(max_length=150)),
                ('address', models.CharField(max_length=500, verbose_name='Adresse')),
                ('postal_code', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(message='Veuillez entrer un code postal valide.', regex='^[0-9]*$')])),
                ('city', models.CharField(max_length=100, verbose_name='Ville')),
                ('telephone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Veuillez entrer un numéro de téléphone valide.', regex='[0-9]{10}')])),
                ('commentaire', models.CharField(blank=True, max_length=1000)),
                ('inactif', models.BooleanField(default=False, verbose_name="Desactivé (Ne cocher que si vous ne souhaitez                                       plus gérer cette personne dans l'application) ")),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('date_accident', models.DateField(blank=True, null=True, verbose_name='Date de l’accident ou de l’apparition des symptômes')),
                ('reason', models.CharField(blank=True, max_length=300, verbose_name='Motif de Consultation')),
                ('symptoms_duration', models.CharField(blank=True, max_length=100, verbose_name='Durée des symptômes')),
                ('summary', models.TextField(blank=True, max_length=500, verbose_name='Bilan ostéopathique')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion.animal', verbose_name='Animal')),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='medical_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='gestion.medicalinfo'),
        ),
        migrations.AddField(
            model_name='animal',
            name='proprietaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion.person', verbose_name='Propriétaire'),
        ),
    ]
