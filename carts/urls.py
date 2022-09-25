from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartAction.as_view()),
    path('cart/<int:pk>/', views.DeleteItem.as_view(), name='cart-delete'),
]