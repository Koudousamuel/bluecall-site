from django.shortcuts import render
from .models import Product, Category, Command
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Command, OrderItem
from django.shortcuts import render, redirect
from django.utils import timezone
import json
from .models import Command, OrderItem
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.http import HttpResponse
import uuid
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Command



def principale(request):
    return render(request, 'green/principale.html')


def index(request):
    product_object = Product.objects.all()
    item_name = request.GET.get('item-name')
    if item_name !='' and item_name is not None:
        product_object = Product.objects.filter(title__icontains=item_name)
    return render(request, 'green/index.html', {'product_object': product_object})



def filtrer_produits(request):
    nom_categorie = request.GET.get('category', None)
    
    if nom_categorie:
        try:
            categorie = Category.objects.get(name__iexact=nom_categorie)  # Insensible à la casse
            produits = Product.objects.filter(category=categorie)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Catégorie introuvable'}, status=404)
    else:
        produits = Product.objects.all()
    
    produits_data = []
    for produit in produits:
        # On choisit l'image locale si disponible, sinon celle depuis Google
        if produit.image_file:
            image_url = produit.image_file.url
        else:
            image_url = produit.images

        produits_data.append({
            'id': produit.id,
            'title': produit.title,
            'price': produit.price,
            'image_url': image_url,
        })
    
    return JsonResponse(produits_data, safe=False)



def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'green/detail.html', {'product_object': product_object})


from django.shortcuts import redirect


@login_required(login_url='green:home') 
def panier_view(request):
    user = request.user
    if request.method == "POST":
        items = request.POST.get('items')
        total = request.POST.get('total')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode = request.POST.get('zipcode')
        taille = request.POST.get('taille')

        # Enregistrer la commande
        com = Command(
            user=user,
            items=items,
            nom=nom,
            email=email,
            address=address,
            ville=ville,
            pays=pays,
            zipcode=zipcode,
            taille=taille,
            total=total
        )
        com.save()

        # Rediriger vers le paiement CinetPay avec l'ID de la commande
        return redirect('green:paytech_payment', commande_id=com.id)

    return render(request, 'green/panier.html', {'user': user})

    
@login_required
def profil(request):
    user = request.user
    return render(request, 'green/profil.html', {'user': user})


def maillot(request):
    try:
        categorie = Category.objects.get(name__iexact='maillots')
        produits = Product.objects.filter(category=categorie)
    except Category.DoesNotExist:
        produits = []

    context = {'product_object': produits}
    return render(request, 'green/maillot.html', context)

def FemmeVet(request):
    try:
        categorie = Category.objects.get(name__iexact='femmevet')
        produits = Product.objects.filter(category=categorie)
    except Category.DoesNotExist:
        produits = []

    context = {'product_object': produits}
    return render(request, 'green/femmevet.html', context)

def sacs(request):
    try:
        categorie = Category.objects.get(name__iexact='sacs')
        produits = Product.objects.filter(category=categorie)
    except Category.DoesNotExist:
        produits = []

    context = {'product_object': produits}
    return render(request, 'green/sacs.html', context)


@login_required
def Historique(request):
    commandes = Command.objects.filter(user=request.user)  # 🔒 Filtre par utilisateur connecté

    for commande in commandes:
        try:
            if isinstance(commande.items, str):
                commande.items = json.loads(commande.items)
            elif not isinstance(commande.items, list):
                commande.items = []
            print(f"✅ Commande {commande.id} items:", commande.items)
        except Exception as e:
            print(f"❌ Erreur de parsing pour la commande {commande.id} :", e)
            commande.items = []

    return render(request, 'green/historique.html', {'commandes': commandes})

def marquer_comme_livree(request, commande_id):
    commande = get_object_or_404(Command, id=commande_id)
    commande.statut = "livrée"
    commande.save()
    return redirect('green:historique') 


def confirmation_view(request):
    return render(request, 'green/confirmation.html')

def condition_view(request):
    return render(request, 'green/condition.html')

def politique_view(request):
    return render(request, 'green/politique.html')

def savoir_view(request):
    return render(request, 'green/savoir.html')



@login_required(login_url='green:home')
def paytech_payment(request, commande_id):
    commande = get_object_or_404(Command, id=commande_id)

    montant = 2000  # ✅ Seulement les frais de livraison

    transaction_id = str(uuid.uuid4())
    commande.transaction_id = transaction_id
    commande.save()

    payload = {
        "command_name": "Paiement Livraison BlueCall",
        "amount": montant,
        "currency": "XOF",
        "ref_command": transaction_id,
        "notification_url": settings.PAYTECH_NOTIFY_URL,
        "return_url": settings.PAYTECH_RETURN_URL,
        "cancel_url": settings.PAYTECH_CANCEL_URL,
        "customer": {
            "name": commande.nom,
            "email": commande.email,
            "phone_number": commande.zipcode
        },
        "items": [
            {
                "item_name": "Frais de livraison",
                "item_price": int(montant),
                "item_quantity": 1
            }
        ],
        "custom_data": {
            "commande_id": commande.id
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "API_KEY": settings.PAYTECH_API_KEY,
        "API_SECRET": settings.PAYTECH_SECRET_KEY
    }

    try:
        response = requests.post("https://paytech.sn/api/payment/request-payment", json=payload, headers=headers, timeout=10)
        data = response.json()

        if data.get("success") and "redirect_url" in data.get("data", {}):
            return redirect(data["data"]["redirect_url"])
        else:
            return HttpResponse("❌ Erreur PayTech : " + str(data), status=500)
    except requests.exceptions.Timeout:
        return HttpResponse("⏳ Délai dépassé lors de la connexion à PayTech.", status=504)
    except Exception as e:
        return HttpResponse("❌ Erreur lors du paiement : " + str(e), status=500)

@csrf_exempt
def paytech_notify(request):
    if request.method == "POST":
        try:
            data = request.POST or json.loads(request.body)

            transaction_id = data.get("ref_command")

            commande = Command.objects.get(transaction_id=transaction_id)
            commande.paye = True
            commande.save()
            return JsonResponse({"status": "✅ Paiement confirmé"})
        except Command.DoesNotExist:
            return JsonResponse({"error": "Commande non trouvée"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return HttpResponse("Méthode non autorisée", status=405)
