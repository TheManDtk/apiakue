from typing import Any, Dict, Tuple
from django.db import models
import uuid
from django.utils import timezone
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
import re

# Create your models here.

class Famille(models.Model):
    familleCode = models.UUIDField(default=uuid.uuid4, editable=False)
    familleLibelle = models.CharField( null = False, max_length=100)
    familleDescription = models.TextField(null = False)
    #is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.familleLibelle

class Categorie(models.Model):
    categorieCode = models.CharField(null = True, blank=True, max_length=100)
    categorieLibelle = models.CharField(null=False ,max_length=100)
    categorieDescription = models.TextField(null = False)
    #is_active = models.BooleanField(default=True)
    famille = models.ForeignKey(Famille, related_name='familles', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if ' ' not in self.categorieLibelle:
            code = self.categorieLibelle[:3] + '01'
        else:
            mots = self.categorieLibelle.split()
            code = ''.join([mot[0] for mot in mots]) + '01'
        self.categorieCode = self.generate_unique_code(code)
        super().save(*args, **kwargs)

    def generate_unique_code(self, code):
        count = 1
        unique_code = code
        while Categorie.objects.filter(categorieCode=unique_code).exists():
            unique_code = code + str(count).zfill(2)
            count += 1
        return unique_code

    def __str__(self):
        return self.categorieLibelle

@receiver(pre_save, sender=Categorie)
def ensure_unique_code(sender, instance, **kwargs):
    instance.categorieCode = instance.generate_unique_code(instance.categorieCode)

class Stock(models.Model):
    quantiteStockSite = models.IntegerField()
    #siteStock = models.ForeignKey(SiteStockage, related_name="siteStocks", on_delete=models.CASCADE,null=True)
    #produit = models.ForeignKey(Produit, related_name="produits", on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'({self.quantiteStockSite})'

class Produit(models.Model):
    produitCode = models.CharField( max_length=20, unique=True, editable=False)
    produitLibelle = models.CharField( max_length=50)
    produitUniteAchat = models.IntegerField( null=True, validators=[MinValueValidator(0)])
    produitUniteVendu = models.IntegerField( null=True, validators=[MinValueValidator(0)])
    produitNivTaxe = models.CharField(null=True, max_length=10,)
    categorie = models.ForeignKey(Categorie, related_name='categories', on_delete=models.CASCADE,null=True )
    stock_item = models.ForeignKey(Stock, related_name='stocks', on_delete=models.PROTECT, null=True)


    def save(self, *args, **kwargs):
        if not self.id:
            prefix = "PRD"
            uuid_str = str(uuid.uuid4().hex)[:8]  # Utilisez les 8 premiers caractères de l'UUID
            produit_prefix = self.produitLibelle[:3].upper()  # Utilisez les trois premières lettres du produit
            self.produitCode = f"{prefix}{uuid_str}{produit_prefix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.produitLibelle



class Departement(models.Model):
    deptLibelle = models.CharField(null=False, max_length=50)
    deptLocalisation = models.CharField(max_length=30)
    deptDateAdd = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.deptLibelle

class Employe(AbstractUser):
    M = "Masculin"
    F = "Féminin"
    CHOIX_SEXE = [(M, "Masculin"), (F, "Féminin"),]
    username = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=17, null=True, unique=True, blank=True)
    employeMatricule = models.CharField(null = True, max_length=100)
    employeDateNaiss = models.DateField(null=True)
    employeAdresse = models.CharField(max_length=100,null=True)
    employeDateEmb = models.DateField(null=True)
    employeSexe = models.CharField( choices = CHOIX_SEXE)
    employePoste = models.CharField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def format_phone_number(self):
            # Replace a space with an empty string
            self.phone_number = re.sub(r"\s", "", self.phone_number)
            # Replace a + with '00'
            self.phone_number = re.sub(r"\+", "00", self.phone_number)
            # Make sure phone_number only contains digits
            self.phone_number = re.sub(r"[^0-9]", "", self.phone_number)
            if not self.phone_number.startswith('00228'):
                self.phone_number = '00228' + self.phone_number

    def save(self, *args, **kwargs):
        if not self.id:
            prefix = "EMP"
            date_str = datetime.now().strftime("%y%m%d")
            nom_initial = self.last_name[:2].upper()
            prenom_initial = self.first_name[:2].upper()
            self.employeMatricule = f"{prefix}{date_str}{nom_initial}{prenom_initial}"

        if self.phone_number:
            self.format_phone_number()
        super().save(*args, **kwargs)

    def delete(self, using = None, keep_parents = False ):
        self.is_active = False
        self.save()

    def __str__(self):
        return f'{self.first_name} ({self.last_name})'

class Admin(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE)

    def __str__(self):
        return self.employe.email    
    
class EmpDept(models.Model):
    empDeptDateStart = models.DateTimeField(auto_now_add=True)
    departement = models.ForeignKey(Departement, related_name='departements', on_delete=models.PROTECT, null=True )
    employe = models.ForeignKey(Employe,related_name='employes', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.departement 

class TypeMouvement(models.Model):
    typeMvtIntitule = models.CharField()
    typeMvtDescription = models.TextField()
    typeAddDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.typeMvtIntitule
    
    
class SiteStockage(models.Model):
    siteStockIntitule = models.CharField( null=False, max_length=30)
    siteStockVille = models.CharField( null=False, max_length=50)
    siteStockDateAdd = models.DateTimeField(auto_now_add=True)
    stockSite = models.ForeignKey(Stock, related_name='stock', on_delete=models.PROTECT)

    def __str__(self):
        return self.siteStockIntitule


class MatriceValidation(models.Model):
    class Meta:
        pass

    libelle = models.CharField()
    nombreValidateur = models.PositiveSmallIntegerField()
    validateur = models.ManyToManyField(Employe,  blank=True)

class TypeValidation(models.Model):
    class Meta:
        pass
    
    libelle = models.CharField()
    matrice = models.OneToOneField(MatriceValidation, on_delete=models.CASCADE)

class Commande(models.Model):
    VALIDE = "Validée"
    EN_COURS = "En cours"
    NON_VALIDE = "Non validée"
    CHOIX_STATUT_VALIDATION = [
        (EN_COURS,"En cours"),
        (VALIDE,"validée"),
        (NON_VALIDE,"Non validée")
    ]
    comTypeValidation = models.ForeignKey(TypeValidation, on_delete=models.CASCADE, null=True)
    comDateAdd = models.DateTimeField(auto_now_add=True)
    comCommentaire = models.TextField()
    employe = models.ForeignKey(Employe, related_name='employeCom', on_delete=models.PROTECT, null=True)
    comStatutValidation = models.CharField(
        choices=CHOIX_STATUT_VALIDATION,
        default=EN_COURS)

    def __str__(self):
        return f'Commande-{self.id}'

class DetailsCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='details_commande')
    detailsComQuantite = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    detailsComPro = models.ForeignKey(Produit, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'({self.detailsComPro}) ({self.detailsComQuantite})'

class Livraison(models.Model):
    livraisonDate = models.DateField()
    commande = models.ForeignKey(Commande, related_name= 'commandes', on_delete= models.CASCADE, null=True )
    
    def __str__(self):
        return self.livraisonDate

class DetailsLivraison(models.Model):
    detailsLivrQte = models.IntegerField()
    livraison = models.ForeignKey(Livraison, related_name= 'livraisons', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.detailsLivrQte
    
class MouvementStock(models.Model):
    mvtStockQuantite = models.IntegerField(null=True)
    mvtStockDate = models.DateTimeField(auto_now_add=True, null=True)
    typeMvt = models.ForeignKey(TypeMouvement, related_name="typeMvts", on_delete=models.CASCADE,null=True)
    livraison = models.ForeignKey(Livraison, related_name="livraisonsMvt", on_delete= models.PROTECT, null=True )

    def __str__(self):
        return f"{self.mvtStockDate} - Quantite: {self.mvtStockQuantite} - Type: {self.typeMvt}"    
#class EmployeDepartement(models.Model):


class DemandeProduit(models.Model):
    VALIDE = "Validée"
    EN_COURS = "En cours"
    NON_VALIDE = "Non validée"
    CHOIX_STATUT_VALIDATION = [
        (EN_COURS,"En cours"),
        (VALIDE,"validée"),
        (NON_VALIDE,"Non validée")
    ]
    demProdDate = models.DateTimeField(auto_now_add=True)
    demProdCommentaire = models.TextField()
    employeDem = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="employesDem", null=True)
    demStatutValidation = models.CharField(
        choices=CHOIX_STATUT_VALIDATION,
        default=EN_COURS)
    
    def __str__(self):
        return f'Demande-{self.id}'


class DetailsDemande(models.Model):
    demande = models.ForeignKey(DemandeProduit, on_delete=models.CASCADE,related_name='details_demande')
    detailsDemQuantite = models.PositiveIntegerField(validators=[MinValueValidator(1)]) 
    detailsDemPro = models.ForeignKey(Produit, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'({self.detailsDemQuantite}) ({self.detailsDemPro})'

    
class Validation(models.Model):
    typeValidation = models.OneToOneField(TypeValidation, on_delete=models.CASCADE)
    dateHeureDeCreation = models.DateTimeField(auto_now_add=True)
    dateValidationTotal = models.DateTimeField(auto_now=True)
    preuveValidations = models.ManyToManyField(Employe, through='PreuveValidation')

    def _str_(self):
        return f"Validation pour {self.typeValidation}"

class PreuveValidation(models.Model):
    validation = models.ForeignKey(Validation, on_delete=models.CASCADE)
    validateur = models.ForeignKey(Employe, on_delete=models.CASCADE)
    dateValidation = models.DateTimeField(default=timezone.now)
    commentaire = models.TextField(blank=True, null=True)