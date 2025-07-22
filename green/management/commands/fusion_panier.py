from django.core.management.base import BaseCommand
from green.models import PanierItem

class Command(BaseCommand):
    help = "Fusionne les doublons dans PanierItem (par user et produit)"

    def handle(self, *args, **kwargs):
        for user_id in PanierItem.objects.values_list('user', flat=True).distinct():
            items = PanierItem.objects.filter(user_id=user_id)
            uniques = {}

            for item in items:
                key = item.produit_id
                if key in uniques:
                    uniques[key].quantite += item.quantite
                    uniques[key].save()
                    item.delete()
                else:
                    uniques[key] = item

        self.stdout.write(self.style.SUCCESS("✅ Fusion des doublons dans PanierItem terminée."))
