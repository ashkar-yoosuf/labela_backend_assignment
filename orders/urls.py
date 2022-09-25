from django.urls import path
from . import views

urlpatterns = [
    path('order/<int:pk>/', views.OrderItems.as_view(), name='order-handler'),
]