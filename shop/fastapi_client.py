import requests
import json
from django.conf import settings
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class FastAPIClient:
    def __init__(self):
        self.base_url = getattr(settings, 'FASTAPI_BASE_URL', 'http://localhost:8001')
        self.timeout = 30
    
    def _make_request(self, method, endpoint, data=None):
        """Make HTTP request to FastAPI"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"FastAPI request failed: {e}")
            raise Exception(f"Failed to communicate with FastAPI: {str(e)}")
    
    def create_item(self, product_data):
        """Create an item in FastAPI from Django product"""
        data = {
            'name': product_data['title'],
            'price': float(product_data['price'])
        }
        return self._make_request('POST', '/items', data)
    
    def create_order(self, order_data):
        """Create an order in FastAPI from Django order"""
        data = {
            'item_id': order_data['item_id'],
            'quantity': order_data['quantity'],
            'status': order_data.get('status', 'pending')
        }
        return self._make_request('POST', '/orders', data)
    
    def create_sale(self, sale_data):
        """Create a sale record in FastAPI"""
        data = {
            'order_id': sale_data['order_id'],
            'total': float(sale_data['total'])
        }
        return self._make_request('POST', '/sales', data)
    
    def get_items(self):
        """Get all items from FastAPI"""
        return self._make_request('GET', '/items')
    
    def get_orders(self):
        """Get all orders from FastAPI"""
        return self._make_request('GET', '/orders')
    
    def get_sales(self):
        """Get all sales from FastAPI"""
        return self._make_request('GET', '/sales')
    
    def sync_order_to_fastapi(self, django_order):
        """Sync a complete Django order to FastAPI"""
        try:
            # First, ensure all products exist in FastAPI as items
            item_mapping = {}  # Map Django product IDs to FastAPI item IDs
            
            for order_item in django_order.items.all():
                product = order_item.product
                
                # Check if item already exists in FastAPI
                existing_items = self.get_items()
                existing_item = None
                for item in existing_items:
                    if item['name'] == product.title and item['price'] == float(product.price):
                        existing_item = item
                        break
                
                if existing_item:
                    item_mapping[product.id] = existing_item['id']
                else:
                    # Create new item in FastAPI
                    item_data = {
                        'title': product.title,
                        'price': float(product.price)
                    }
                    new_item = self.create_item(item_data)
                    item_mapping[product.id] = new_item['id']
            
            # Create orders in FastAPI for each order item
            fastapi_order_ids = []
            for order_item in django_order.items.all():
                order_data = {
                    'item_id': item_mapping[order_item.product.id],
                    'quantity': order_item.quantity,
                    'status': django_order.status
                }
                fastapi_order = self.create_order(order_data)
                fastapi_order_ids.append(fastapi_order['id'])
            
            # Create sale record for the total order
            if fastapi_order_ids:
                sale_data = {
                    'order_id': fastapi_order_ids[0],  # Use first order ID as reference
                    'total': float(django_order.total_amount)
                }
                self.create_sale(sale_data)
            
            logger.info(f"Successfully synced Django order {django_order.id} to FastAPI")
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync Django order {django_order.id} to FastAPI: {e}")
            return False
