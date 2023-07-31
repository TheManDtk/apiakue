# Generated by Django 4.2.3 on 2023-07-28 14:37

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.EmailField(max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, unique=True)),
                ('employeMatricule', models.CharField(max_length=100, null=True)),
                ('employeDateNaiss', models.DateField(null=True)),
                ('employeAdresse', models.CharField(max_length=100, null=True)),
                ('employeDateEmb', models.DateField(null=True)),
                ('employeSexe', models.CharField(choices=[('Masculin', 'Masculin'), ('Féminin', 'Féminin')])),
                ('employePoste', models.CharField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorieCode', models.CharField(blank=True, max_length=100, null=True)),
                ('categorieLibelle', models.CharField(max_length=100)),
                ('categorieDescription', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comDateAdd', models.DateTimeField(auto_now_add=True)),
                ('comCommentaire', models.TextField()),
                ('employe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employeCom', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DemandeProduit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('demProdDate', models.DateTimeField(auto_now_add=True)),
                ('demProdCommentaire', models.TextField()),
                ('employeDem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employesDem', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deptLibelle', models.CharField(max_length=50)),
                ('deptLocalisation', models.CharField(max_length=30)),
                ('deptDateAdd', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('familleCode', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('familleLibelle', models.CharField(max_length=100)),
                ('familleDescription', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Livraison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('livraisonDate', models.DateField()),
                ('commande', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='akueapi.commande')),
            ],
        ),
        migrations.CreateModel(
            name='MatriceValidation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField()),
                ('nombreValidateur', models.PositiveSmallIntegerField()),
                ('validateur', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PreuveValidation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateValidation', models.DateTimeField(default=django.utils.timezone.now)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('validateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantiteStockSite', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeMouvement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeMvtIntitule', models.CharField()),
                ('typeMvtDescription', models.TextField()),
                ('typeAddDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeValidation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField()),
                ('matrice', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='akueapi.matricevalidation')),
            ],
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateHeureDeCreation', models.DateTimeField(auto_now_add=True)),
                ('dateValidationTotal', models.DateTimeField(auto_now=True)),
                ('preuveValidations', models.ManyToManyField(through='akueapi.PreuveValidation', to=settings.AUTH_USER_MODEL)),
                ('typeValidation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='akueapi.typevalidation')),
            ],
        ),
        migrations.CreateModel(
            name='SiteStockage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('siteStockIntitule', models.CharField(max_length=30)),
                ('siteStockVille', models.CharField(max_length=50)),
                ('siteStockDateAdd', models.DateTimeField(auto_now_add=True)),
                ('stockSite', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock', to='akueapi.stock')),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produitCode', models.CharField(editable=False, max_length=20, unique=True)),
                ('produitLibelle', models.CharField(max_length=50)),
                ('produitUniteAchat', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('produitUniteVendu', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('produitNivTaxe', models.CharField(max_length=10, null=True)),
                ('categorie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='akueapi.categorie')),
                ('stock_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='stocks', to='akueapi.stock')),
            ],
        ),
        migrations.AddField(
            model_name='preuvevalidation',
            name='validation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akueapi.validation'),
        ),
        migrations.CreateModel(
            name='MouvementStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mvtStockQuantite', models.IntegerField(null=True)),
                ('mvtStockDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('livraison', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='livraisonsMvt', to='akueapi.livraison')),
                ('typeMvt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='typeMvts', to='akueapi.typemouvement')),
            ],
        ),
        migrations.CreateModel(
            name='EmpDept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empDeptDateStart', models.DateTimeField(auto_now_add=True)),
                ('departement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='departements', to='akueapi.departement')),
                ('employe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetailsLivraison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailsLivrQte', models.IntegerField()),
                ('livraison', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='livraisons', to='akueapi.livraison')),
            ],
        ),
        migrations.CreateModel(
            name='DetailsDemande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailsDemQuantite', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('demande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akueapi.demandeproduit')),
                ('detailsDemPro', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='akueapi.produit')),
            ],
        ),
        migrations.CreateModel(
            name='DetailsCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailsComQuantite', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details_commande', to='akueapi.commande')),
                ('detailsComPro', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='akueapi.produit')),
            ],
        ),
        migrations.AddField(
            model_name='categorie',
            name='famille',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='familles', to='akueapi.famille'),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]