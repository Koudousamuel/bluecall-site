from django.contrib import admin
from .models import Category, Product, Command
from django.utils.html import format_html

# Aperçu image dans admin pour Category
admin.site.site_header = "Blue Call-Multicolore"
admin.site.site_title = "Blue Call"
admin.site.index_title = "Administration"


class AdminCategorie(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'image_preview')

    def image_preview(self, obj):
        if obj.get_image():
            return format_html('<img src="{}" style="height: 50px;" />', obj.get_image())
        return "Pas d'image"
    image_preview.short_description = "Aperçu"

class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'date_added')
    search_fields = ('title',)
    list_editable = ('price',)

# Action personnalisée pour marquer la commande comme livrée
@admin.action(description="Marquer comme livrée")
def marquer_comme_livree(modeladmin, request, queryset):
    queryset.update(statut='livrée')

class AdminCommand(admin.ModelAdmin):
    list_display = ('items', 'total', 'nom', 'address', 'email', 'ville', 'pays', 'zipcode', 'date_command', 'taille', 'statut')
    actions = [marquer_comme_livree]  # Ajouter l'action de mise à jour du statut

# Enregistrement des modèles dans l'admin
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategorie)
admin.site.register(Command, AdminCommand)
