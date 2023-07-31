from rest_framework import serializers
from akueapi.models import *
from django.forms import ValidationError
#from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['id','produitCode','produitLibelle','produitUniteAchat','produitUniteVendu','produitNivTaxe','categorie']
        extra_kwargs = {
            'produitCode': {'read_only': True},
            'id':  {'read_only': True}
        }


class CategorieSerializer(serializers.ModelSerializer):
    categorie = ProduitSerializer(many = True,source='categories', read_only = True)
    
    class Meta:
        model = Categorie
        fields = ['id','categorieLibelle','categorieCode','categorieDescription','famille','categorie']
        extra_kwargs = {
            'categorieCode': {'read_only': True},
            'id':  {'read_only': True},
            'produit':{'read_only': True},
        }

class FamilleSerializer(serializers.ModelSerializer):
    famille = CategorieSerializer(many=True, source='familles')

    class Meta:
        model = Famille
        fields = ['id','familleCode','familleLibelle', 'familleDescription', 'famille']
        extra_kwargs = {
            'familleCode': {'read_only': True},
            'id':  {'read_only': True},
            'famille':{'read_only': True}
        }


class EmployeSerializer(serializers.ModelSerializer):
    password = serializers.CharField( required=True, validators=[validate_password])
    class Meta:
        model = Employe
        fields = ['id','username','last_name','first_name','password', 'phone_number', 'employeMatricule', 'employeDateNaiss', 'employeAdresse', 'employeDateEmb','employeSexe', 'employePoste']
        extra_kwargs = {
            'employeMatricule': {'read_only': True},
            'id':  {'read_only': True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password')
        employe = Employe(**validated_data)
        employe.set_password(password)
        employe.save()
        return employe


class EmpDeptSerializer(serializers.ModelSerializer):
    employe = EmployeSerializer()
    
    class Meta:
        model = EmpDept
        fields = '__all__'



class DepartementSerializer(serializers.ModelSerializer):
    #affectation = EmpDeptSerializer()
    
    class Meta:
        model = Departement
        fields = '__all__'

class MouvementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouvementStock
        fields = "__all__"

class TypeMvtSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeMouvement
        fields = "__all__"

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"

class SiteStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStockage
        fields = "__all__"

class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

class DetailsCommandeSerializer(serializers.ModelSerializer):
    detailsComPro = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all())

    class Meta:
        model = DetailsCommande
        fields = ['detailsComQuantite','detailsComPro']


class CommandeSerializer(serializers.ModelSerializer):
    details_commande = DetailsCommandeSerializer(many=True)

    class Meta:
        model = Commande
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details_commande')
        commande = Commande.objects.create(**validated_data)
        for detail_data in details_data:
            DetailsCommande.objects.create(commande=commande, **detail_data)
        return commande
    


class DetailsDemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailsDemande
        fields = ['detailsDemPro','detailsDemQuantite']


class DemandeSerializer(serializers.ModelSerializer):
    details_demande = DetailsDemandeSerializer(many=True)

    class Meta:
        model = DemandeProduit
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details_demande')
        demande = DemandeProduit.objects.create(**validated_data)
        for detail_data in details_data:
            DetailsDemande.objects.create(demande=demande, **detail_data)
        return demande
    


class MatriceValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatriceValidation
        fields = '__all__'

class TypeValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeValidation
        fields = '__all__'

class ValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = '__all__'