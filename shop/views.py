from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.http import HttpResponse
from .models import Category, Product, Order, OrderItem
from .forms import SignUpForm, AddToCartForm, CheckoutForm
from .cart import Cart
from .fastapi_client import FastAPIClient
import logging

logger = logging.getLogger(__name__)

def product(request,pk):
    products = Product.objects.get(id=pk)
    return render(request, "product.html", {"products": products})

def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In..."))
            return redirect('shop:home')
        else:
            messages.success(request, ("There was an error, please try again..."))
            return redirect('shop:login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out..."))
    return redirect('shop:home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have Registered Successfully!! Welcome!..."))
            return redirect('shop:home')
        else:
            messages.success(request, ("There was a problem Registering, please try again!..."))
            return redirect('shop:register')
    else:
        return render(request, 'register.html', {'form':form})


def product_list(request, slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    category = None
    query = request.GET.get('q')
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
    if query:
        products = products.filter(title__icontains=query)
    context = {'categories': categories, 'products': products, 'category': category, 'query': query or ''}
    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = AddToCartForm()
    return render(request, 'shop/product.html', {'product': product})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    qty = int(request.POST.get('quantity', 1))
    cart.add(product_id, qty)
    messages.success(request, 'Item added to cart.')
    return redirect('shop:cart_detail')

def cart_update(request, product_id):
    cart = Cart(request)
    qty = int(request.POST.get('quantity', 1))
    cart.add(product_id, qty, update_quantity=True)
    messages.success(request, 'Cart updated.')
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.info(request, 'Item removed from cart.')
    return redirect('shop:cart_detail')

@transaction.atomic
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                guest_email=None if request.user.is_authenticated else data.get('email'),
                guest_name=None if request.user.is_authenticated else data.get('name'),
                shipping_name=data['name'],
                shipping_address1=data['address1'],
                shipping_address2=data.get('address2', ''),
                shipping_city=data['city'],
                shipping_postal_code=data['postal_code'],
                shipping_country=data['country'],
                paid=False,
                status='new'
            )
            # create order items and reduce inventory
            for item in cart:
                if item['quantity'] > item['product'].inventory:
                    transaction.set_rollback(True)
                    messages.error(request, f"Insufficient inventory for {item['product'].title}. Available: {item['product'].inventory}")
                    return redirect('shop:cart_detail')
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
                item['product'].inventory -= item['quantity']
                item['product'].save()
            
            # Sync order to FastAPI
            try:
                fastapi_client = FastAPIClient()
                sync_success = fastapi_client.sync_order_to_fastapi(order)
                if sync_success:
                    logger.info(f"Order {order.id} successfully synced to FastAPI")
                else:
                    logger.warning(f"Failed to sync order {order.id} to FastAPI, but order was created in Django")
            except Exception as e:
                logger.error(f"Error syncing order {order.id} to FastAPI: {e}")
                # Don't fail the order creation if FastAPI sync fails
                pass
            
            cart.clear()
            messages.success(request, 'Order placed successfully.')
            return redirect('shop:order_success', order_id=order.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email
            initial['name'] = request.user.get_full_name() or request.user.username
        form = CheckoutForm(initial=initial)

    return render(request, 'shop/checkout.html', {'cart': cart, 'form': form})

def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'shop/order_success.html', {'order': order})

def test_fastapi_connection(request):
    """Test view to check FastAPI connection and display data"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('shop:product_list')
    
    try:
        fastapi_client = FastAPIClient()
        
        # Test connection and get data
        items = fastapi_client.get_items()
        orders = fastapi_client.get_orders()
        sales = fastapi_client.get_sales()
        
        context = {
            'items': items,
            'orders': orders,
            'sales': sales,
            'connection_status': 'Connected'
        }
        
        messages.success(request, 'Successfully connected to FastAPI!')
        
    except Exception as e:
        context = {
            'items': [],
            'orders': [],
            'sales': [],
            'connection_status': f'Error: {str(e)}'
        }
        messages.error(request, f'Failed to connect to FastAPI: {str(e)}')
    
    return render(request, 'shop/fastapi_test.html', context)
