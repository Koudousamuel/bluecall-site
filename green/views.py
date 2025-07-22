from django.shortcuts import render
from .models import Product, Category, Command, PanierItem 
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

@login_required(login_url='green:home')
def panier_view(request):
    user = request.user

    if request.method == "POST":
        # ✅ Récupérer les données du formulaire
        items_json = request.POST.get('items')
        total = request.POST.get('total')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode = request.POST.get('zipcode')
        taille = request.POST.get('taille')

        # ✅ Créer la commande principale
        commande = Command.objects.create(
            user=user,
            items=items_json,
            nom=nom,
            email=email,
            address=address,
            ville=ville,
            pays=pays,
            zipcode=zipcode,
            taille=taille,
            total=total,
            date_command=timezone.now()
        )

        # ✅ Parser les items et créer les OrderItem
        try:
            items = json.loads(items_json)
            for item in items:
                produit_nom = item.get('nom')
                quantite = int(item.get('quantite', 1))
                prix = float(item.get('prix', 0))

                # ✅ Corrigé : éviter l'erreur MultipleObjectsReturned
                produit = Product.objects.filter(title=produit_nom).first()
                if produit:
                    OrderItem.objects.create(
                        command=commande,
                        product_nom=produit,
                        quantity=quantite,
                        price=prix
                    )
                else:
                    print(f"Produit introuvable : {produit_nom}")

        except json.JSONDecodeError as e:
            print("Erreur JSON dans les items du panier :", e)

        # ✅ Vider le panier après la commande
        PanierItem.objects.filter(user=user).delete()

        return redirect('green:confirmation')

    # 👇 cas GET : afficher le contenu du panier
    items = PanierItem.objects.filter(user=user)
    total = sum(item.produit.price * item.quantite for item in items)
    total_quantite = sum(item.quantite for item in items)

    return render(request, 'green/panier.html', {
        'user': user,
        'items': items,
        'total': total,
        'total_quantite': total_quantite
    })




@login_required
def panier_popover_data(request):
    panier_items = PanierItem.objects.filter(user=request.user)
    data = []

    for item in panier_items:
        data.append({
            'nom': item.produit.title,
            'quantite': item.quantite
        })

    return JsonResponse({'panier': data})

@login_required
def ajouter_au_panier(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            produit_id = data.get('produit_id')
            produit = Product.objects.get(id=produit_id)
        except (Product.DoesNotExist, ValueError, KeyError):
            return JsonResponse({'status': 'error', 'message': 'Produit introuvable ou données invalides'}, status=400)

        user = request.user

        item, created = PanierItem.objects.get_or_create(user=user, produit=produit)

        if not created:
            item.quantite += 1
            item.save()

        total = PanierItem.objects.filter(user=user).count()

        return JsonResponse({'status': 'success', 'message': 'Ajouté au panier', 'total': total})

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)


@login_required
def vider_panier(request):
    PanierItem.objects.filter(user=request.user).delete()
    return redirect('green:panier') 



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