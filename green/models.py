from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    image_file = models.ImageField(upload_to='categories/', blank=True, null=True)  # <-- Ajouté ici
    date_added = models.DateField(auto_now=True)
    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name
    
    def get_image(self):
        if self.image_file:
            return self.image_file.url  # image locale si elle existe
        return None

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='categorie', on_delete=models.CASCADE)
    images = models.CharField(max_length=5000, blank=True, null=True)
    image_file = models.ImageField(upload_to='products/', blank=True, null=True)  # image locale
    date_added = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title
    
    def get_image(self):
        if self.image_file:
            return self.image_file.url  # image locale si elle existe
        return self.images 
    
class Command(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    items = models.CharField(max_length=300)
    total = models.CharField(max_length=200)
    nom = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    ville = models.CharField(max_length=300)
    pays = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=300)
    taille = models.CharField(max_length=50)
    statut = models.CharField(max_length=100, default='livraison en cours')
    date_command = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Commande {self.id} - {self.nom}"

    def get_products(self):
        return self.orderitem_set.all() 
    
class OrderItem(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    product_nom = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Quantité du produit commandé
    price = models.FloatField()  # Prix du produit au moment de la commande

    def __str__(self):
        return f"{self.product.title} x{self.quantity}"