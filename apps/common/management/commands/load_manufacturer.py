import json

from django.core.management.base import BaseCommand

from apps.common.models import Manufacturer


class Command(BaseCommand):
    help = "Loads Manufacturer if they are not loaded"

    def handle(self, *args, **options):
        with open("apps/common/management/commands/manufacturer.json", "r", encoding="UTF-8") as f:
            make_data = json.load(f)
            for data in make_data:
                try:
                    if not Manufacturer.objects.filter(id=data["id"]).exists():
                        make = Manufacturer.objects.create(id=data["id"], name=data["name"])
                        self.stdout.write(self.style.SUCCESS(f'{data["name"]} has been created'))
                    else:
                        self.stdout.write(self.style.WARNING(f'{data["name"]} is already exists'))
                except Exception as e:
                    print({"error": e})
                    break
            self.stdout.write(self.style.SUCCESS("Car Manufacturer has been loaded"))
