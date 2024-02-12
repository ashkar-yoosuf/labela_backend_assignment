from django.core.management.base import BaseCommand
import pandas as pd
from autoparts.models import Product

class Command(BaseCommand):
    help = 'import booms'
    
    def add_argument(self, parser):
        pass

    def handle(self, *args, **options):
        df = pd.read_csv('parts.csv')
        for ID, NAME, DETAILS in zip(df.id, df.name, df.details):
            product_record = Product(id=ID, name=NAME, details=DETAILS)
            product_record.save()

        self.stdout.write('Populated initial product details')
