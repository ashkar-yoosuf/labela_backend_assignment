from django.urls import path
from . import views

urlpatterns = [
    path('cart/<int:pk>/', views.cartList, name='cart'),
    path('deliver/<int:pk>/', views.deliver, name='deliver')
]