from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Manage product inventory levels'

    def add_arguments(self, parser):
        parser.add_argument(
            '--product-id',
            type=int,
            help='Product ID to update inventory for',
        )
        parser.add_argument(
            '--product-title',
            type=str,
            help='Product title to update inventory for',
        )
        parser.add_argument(
            '--set-inventory',
            type=int,
            help='Set inventory to specific amount',
        )
        parser.add_argument(
            '--add-inventory',
            type=int,
            help='Add amount to current inventory',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all products with their inventory levels',
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_inventory()
            return

        if not options['set_inventory'] and not options['add_inventory']:
            self.stdout.write(
                self.style.ERROR('Please specify --set-inventory or --add-inventory')
            )
            return

        # Find the product
        product = None
        if options['product_id']:
            try:
                product = Product.objects.get(id=options['product_id'])
            except Product.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Product with ID {options["product_id"]} not found')
                )
                return
        elif options['product_title']:
            try:
                product = Product.objects.get(title__icontains=options['product_title'])
            except Product.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Product with title containing "{options["product_title"]}" not found')
                )
                return
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --product-id or --product-title')
            )
            return

        # Update inventory
        if options['set_inventory'] is not None:
            product.inventory = options['set_inventory']
            product.save()
            self.stdout.write(
                self.style.SUCCESS(f'Set {product.title} inventory to {product.inventory}')
            )
        elif options['add_inventory'] is not None:
            product.inventory += options['add_inventory']
            product.save()
            self.stdout.write(
                self.style.SUCCESS(f'Added {options["add_inventory"]} to {product.title}. New inventory: {product.inventory}')
            )

    def list_inventory(self):
        products = Product.objects.all().order_by('title')
        self.stdout.write('\nCurrent Inventory Levels:')
        self.stdout.write('-' * 50)
        for product in products:
            status = self.style.SUCCESS('✓') if product.inventory > 0 else self.style.ERROR('✗')
            self.stdout.write(f'{status} {product.title}: {product.inventory}')
        self.stdout.write('-' * 50)
