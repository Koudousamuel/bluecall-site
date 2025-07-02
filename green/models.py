from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField  # <-- Ajouté

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    image_file = CloudinaryField('image', blank=True, null=True)  # <-- Modifié ici
    date_added = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image_file:
            return self.image_file.url
        return None


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='categorie', on_delete=models.CASCADE)
    images = models.CharField(max_length=5000, blank=True, null=True)
    image_file = CloudinaryField('image', blank=True, null=True)  # <-- Modifié ici
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title
    @property
    def get_image(self):
        if self.image_file:
            return self.image_file.url
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

    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paye = models.BooleanField(default=False)  # Ce

    def __str__(self):
        return f"Commande {self.id} - {self.nom}"

    def get_products(self):
        return self.orderitem_set.all()


class OrderItem(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    product_nom = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product_nom.title} x{self.quantity}"
    
