from django.urls import path
from green.views import index, detail
from . import views

app_name = 'green'

urlpatterns = [
    path('reset-admin/', views.reset_admin_password, name='reset_admin'),
    path('', views.principale, name='home'),
    path('index/', views.index, name='index'),
    path('filtrer-produits/', views.filtrer_produits, name='filtrer_produits'),
    path('<int:myid>/', views.detail, name='detail'),
    path('panier/', views.panier_view, name='panier'),
    path('profil/', views.profil, name='profil'),
    path('Maillots/', views.maillot, name='maillot'),
    path('Vetements-Femmes/', views.FemmeVet , name='femmevet'),
    path('Sacs-Homme/', views.sacs , name='sacs'),
    path('Historique/', views.Historique , name='historique'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
    path('Conditions Générales/', views.condition_view, name='condition'),
    path('Politique de Confidentialité/', views.politique_view, name='politique'),
    path('A propos/', views.savoir_view, name='savoir'),
    path('commande/<int:commande_id>/livree/', views.marquer_comme_livree, name='marquer_comme_livree'),
    path('ajouter-au-panier/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('ajax/panier-popover/', views.panier_popover_data, name='panier_popover'),
    path('vider-panier/', views.vider_panier, name='vider_panier'),

]

