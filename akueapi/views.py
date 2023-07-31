from django.shortcuts import render

# Create your views here.
from django.middleware.csrf import get_token
from django.shortcuts import render
from akueapi.models import *
from rest_framework.views import APIView
from akueapi.serializers import *
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate, login, logout,get_user_model
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ProductList(APIView):
    def get(self, request):
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
class CreateProduct(APIView):
    def post(self,request):
        serializer = ProduitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CategorieList(APIView):
    def get(self, request):
        categories = Categorie.objects.all()
        serializer = CategorieSerializer(categories, many = True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

class CreateCategory(APIView):
    def post(self, request):
        serializer = CategorieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class FamilyList(APIView):
    def get(self,request):
        familles = Famille.objects.all()
        serializer = FamilleSerializer(familles, many = True)
        return Response(serializer.data)

class CreateFamille(APIView):
    def post(self, request):
        serializer = FamilleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CreateEmpDept(APIView):
    def post(self, request):
        serializer = EmpDeptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateEmploye(APIView):
    def post(self, request, format=None):
        serializer = EmployeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ObtenirEmploye(APIView):
    def get(self,request):
        employes = Employe.objects.all()
        serializer = EmployeSerializer(employes, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateDepartement(APIView):
    def post(self, request):
        serializer = DepartementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""   
class EmployeLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        passde = Employe.objects.filter(email=email)
        serialize = EmployeSerializer(passde)
        employe = authenticate(request, username=email, password=password)
        if employe is not None:
            login(request, employe)
            return Response({'message': 'Connexion réussie'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
""" 
class CommandeListCreateView(APIView):
    def post(self, request, format=None):
        serializer = CommandeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommmandeListOnly(APIView):
    def get(self, request):
        commande = Commande.objects.all()
        serializer = CommandeSerializer(commande, many = True)
        return Response(
            serializer.data
        )
    

class CommandeListCreateView(APIView):
    def post(self, request, format=None):
        serializer = CommandeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommmandeListOnly(APIView):
    def get(self, request):
        commande = Commande.objects.all()
        serializer = CommandeSerializer(commande, many = True)
        return Response(
            serializer.data
        )
    
class CommandeEmploye(APIView):
    def get(self, request, employe, format = None):
        commandes = Commande.objects.filter(employe = employe)
        serializer = CommandeSerializer(commandes, many = True)
        return Response(
            serializer.data
        )
    
class DemandeListCreateView(APIView):
    def post(self, request, format=None):
        serializer = DemandeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status= status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class DemandeListOnly(APIView):
    def get(self, request):
        demande = DemandeProduit.objects.all()
        serializer = DemandeSerializer(demande, many = True)
        return Response(
            serializer.data
        )
    

class EmployeLogin(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
    #   username = request.data['username']
    #   password = request.data['password']
        print("Received data - username:", username)
        print("Received data - password:", password)
        employe = authenticate(username = username, password = password)
        print("User authenticated successfully:", employe)

        print("Received data - username:", username)
        print("Received data - password:", password)
        if employe:
            print("User authenticated successfully:", employe)
            serializer= EmployeSerializer(employe)
            login(request, employe)
            data = {
                "message": "connexion réussie",
                "employe": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK,)
        else:
            data = {
                "message": "identifiants invalides"
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        
class EmployeLogout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        data = {
            "message": "déconnexion réussie"
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        logout(request)
        data = {
            "message": "déconnexion réussie"
        }
        return Response(data, status=status.HTTP_200_OK)



class CommandeValidationView(APIView):
    def get(self, request, format=None):
        # Récupérer la note de frais en cours de traitement pour le validateur actuel
        validateur_actuel = request.user  # Supposons que le validateur est l'utilisateur connecté
        commande = Commande.objects.filter(
            comStatutValidation='En cours',
            comTypeValidation__matrice__validateur=validateur_actuel,
        ).first()

        if commande:
            serializer = CommandeSerializer(commande)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Aucune commande en cours de traitement pour vous.'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_context(self):
        # Obtenir le token CSRF
        csrf_token = get_token(self.request)
        return {'csrf_token': csrf_token}

    def post(self, request, format=None):
        # Récupérer la note de frais en cours de traitement pour le validateur actuel
        validateur_actuel = request.user  # Supposons que le validateur est l'utilisateur connecté
        commande = Commande.objects.filter(
            comStatutValidation='En cours',
            comTypeValidation__matrice__validateur=validateur_actuel,
        ).first()

        if commande:
            # Vérifier si le validateur approuve ou refuse la note de frais
            approuve = request.data.get('approuve')
            if approuve:
                # Marquer le validateur actuel comme ayant validé la note de frais
                validation = Validation.objects.get(typeValidation=commande.comTypeValidation)
                preuve_validation = PreuveValidation.objects.create(
                    validation=validation,
                    validateur=validateur_actuel,
                )
                validation.preuveValidations.add(preuve_validation)

                # Vérifier si tous les validateurs ont validé la note de frais
                if validation.preuveValidations.count() == validation.typeValidation.matrice.nombreValidateur:
                    # Marquer la note de frais comme validée
                    commande.comStatutValidation = 'Validée'
                    commande.save()

                return Response({'detail': 'La commande a été validée.'}, status=status.HTTP_200_OK)
            else:
                # Le validateur a refusé la note de frais
                commentaire = request.data.get('commentaire')
                validation = Validation.objects.get(typeValidation=commande.comTypeValidation)
                preuve_validation = PreuveValidation.objects.create(
                    validation=validation,
                    validateur=validateur_actuel,
                    commentaire=commentaire,
                )
                validation.preuveValidations.add(preuve_validation)

                # Marquer la note de frais comme non validée
                commande.comStatutValidation = 'Non validée'
                commande.save()

                return Response({'detail': 'La note de frais a été refusée.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Aucune note de frais en cours de traitement pour vous.'}, status=status.HTTP_404_NOT_FOUND)