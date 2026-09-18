import json
from pathlib import Path

from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    help = "Import products from products_data.json"

    def handle(self, *args, **options):
        file_path = Path("products_data.json")

        if not file_path.exists():
            self.stdout.write(
                self.style.ERROR("products_data.json not found")
            )
            return

        data = json.loads(
            file_path.read_text(encoding="utf-8")
        )

        count = 0

        for item in data:
            if item.get("model") != "store.product":
                continue

            Product.objects.update_or_create(
                pk=item["pk"],
                defaults=item["fields"],
            )

            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {count} products successfully."
            )
        )

       