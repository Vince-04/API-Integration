from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>/', views.product_detail, name='product'),
    path('', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.product_list, name='product_list_by_category'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]
