import json

from django.core.management.base import BaseCommand

from apps.common.models import CarModel


class Command(BaseCommand):
    help = "Loads models if they are not loaded"

    def handle(self, *args, **options):
        with open("apps/common/management/commands/car_model.json", "r", encoding="UTF-8") as f:
            model_data = json.load(f)
            for data in model_data:
                try:
                    name = data["model"]
                    if not name:
                        continue
                    if not CarModel.objects.filter(id=data["id"]).exists():
                        CarModel.objects.get_or_create(id=data["id"], name=name, manufacturer_id=data["mark_id"])
                        self.stdout.write(self.style.SUCCESS(f'{data["model"]} has been created'))
                    else:
                        self.stdout.write(self.style.WARNING(f'{data["model"]} is already exists'))
                except Exception as e:
                    print({"error": e})
            self.stdout.write(self.style.SUCCESS("Car Makes has been loaded"))
