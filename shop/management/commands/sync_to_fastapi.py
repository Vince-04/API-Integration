from django.core.management.base import BaseCommand
from shop.models import Order
from shop.fastapi_client import FastAPIClient
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync existing Django orders to FastAPI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--order-id',
            type=int,
            help='Sync specific order by ID',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Sync all orders',
        )

    def handle(self, *args, **options):
        fastapi_client = FastAPIClient()
        
        if options['order_id']:
            try:
                order = Order.objects.get(id=options['order_id'])
                self.sync_order(fastapi_client, order)
            except Order.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Order {options["order_id"]} not found')
                )
        elif options['all']:
            orders = Order.objects.all()
            self.stdout.write(f'Syncing {orders.count()} orders to FastAPI...')
            for order in orders:
                self.sync_order(fastapi_client, order)
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --order-id or --all')
            )

    def sync_order(self, fastapi_client, order):
        try:
            success = fastapi_client.sync_order_to_fastapi(order)
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully synced order {order.id}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Failed to sync order {order.id}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error syncing order {order.id}: {e}')
            )
