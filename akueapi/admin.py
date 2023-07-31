
from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Employe, 
                Famille, 
                Categorie, 
                Produit,
                Stock,
                EmpDept, 
                DemandeProduit, 
                Commande,
                Livraison,
                DetailsLivraison,
                DetailsDemande,
                SiteStockage, 
                DetailsCommande,
                Departement,
                MouvementStock, 
                TypeValidation,
                MatriceValidation,
                PreuveValidation,
                Validation,

TypeMouvement)
class GenericAdmin(admin.ModelAdmin):
    pass
