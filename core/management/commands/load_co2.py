import csv
from datetime import date
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import CO2

class Command(BaseCommand):
    help = 'Load data from CO2 file'

    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'data' / 'co2_mm_mlo.csv'

        with open(datafile, newline='') as csvfile:
            reader = csv.DictReader(islice(csvfile, 51, None))
            for row in reader:
                dt = date(
                    year=int(row['year']),
                    month=int(row['month']),
                    day=1
                )
                # Converter average para float
                average = float(row['average']) if row['average'] else None
                
                # Use get_or_create para inserir os dados
                CO2.objects.get_or_create(date=dt, average=average)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))