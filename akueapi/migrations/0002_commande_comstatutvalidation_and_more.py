# Generated by Django 4.2.3 on 2023-07-29 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('akueapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='comStatutValidation',
            field=models.CharField(choices=[('En cours', 'En cours'), ('Validée', 'validée'), ('Non validée', 'Non validée')], default='En cours'),
        ),
        migrations.AddField(
            model_name='demandeproduit',
            name='demStatutValidation',
            field=models.CharField(choices=[('En cours', 'En cours'), ('Validée', 'validée'), ('Non validée', 'Non validée')], default='En cours'),
        ),
        migrations.AlterField(
            model_name='detailsdemande',
            name='demande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details_demande', to='akueapi.demandeproduit'),
        ),
        migrations.AlterField(
            model_name='detailsdemande',
            name='detailsDemPro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='akueapi.produit'),
        ),
    ]
