# Generated by Django 4.2.3 on 2023-07-29 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('akueapi', '0002_commande_comstatutvalidation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailscommande',
            name='detailsComPro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='akueapi.produit'),
        ),
    ]
