from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('summary/', views.cart_summary, name="cart_summary"),
    path('add/', views.cart_add, name="cart_add"),
    path("delete/<int:product_id>/", views.cart_delete, name="cart_delete"),
    path("update/<int:product_id>/", views.cart_update, name="cart_update"),
    path('checkout/', views.checkout, name='cart_checkout'),
    #path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]
