import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from core.models import AccessLog

class Command(BaseCommand):
    help = 'Generate fake access logs'

    def handle(self, *args, **kwargs):
        services = ['Home', 'Dashboard', 'Profile', 'Settings', 'Reports']
        start_date = datetime.now() - timedelta(days=30)  # Últimos 30 dias
        end_date = datetime.now()

        for _ in range(100):  # Gerar 100 registros
            timestamp = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
            service_name = random.choice(services)
            AccessLog.objects.create(timestamp=timestamp, service_name=service_name)
        
        self.stdout.write(self.style.SUCCESS('Successfully generated fake access logs'))
        
        
        
# python manage.py generate_fake_access_logs
