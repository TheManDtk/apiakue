
from django.contrib import admin
from django.urls import path
from akueapi.views import *

urlpatterns = [
    path('api/auth/login/', EmployeLogin.as_view(), name = 'login'),
    path('api/auth/employe/create/', CreateEmploye.as_view()),
    path('api/auth/departement/create/', CreateDepartement.as_view()),
    path('api/auth/emptdept/create/', CreateEmpDept.as_view()),
    path('api/auth/products/', ProductList.as_view()),
    path('api/auth/product/new', CreateProduct.as_view()),
    path('api/auth/categories/', CategorieList.as_view()),
    path('api/auth/category/new', CreateCategory.as_view()),
    path('api/auth/families/', FamilyList.as_view()),
    path('api/auth/family/new', CreateFamille.as_view()),
    path('api/auth/employeliste/', ObtenirEmploye.as_view()),
    path('api/auth/commande/new', CommandeListCreateView.as_view(), name='commande-list-create'),
    path('api/auth/commandes/', CommmandeListOnly.as_view()),
    path('api/auth/demande/new', DemandeListCreateView.as_view()),
    path('api/auth/demandes/', DemandeListOnly.as_view()),
    path('api/auth/commandes/employe/<int:employe>', CommandeEmploye.as_view()),
    path('validation/', CommandeValidationView.as_view(), name='Commande_validation'),



]
