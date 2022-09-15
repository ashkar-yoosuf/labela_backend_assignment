from django.urls import path
from .views import ProductListView
from . import views

urlpatterns = [
    path('', ProductListView.as_view(), name='autopart-home'),
    path('product/<int:pk>/', views.detail, name='product-detail'),
    path('product/<int:pk>/<int:cart_id>/delete', views.delete, name='product-delete'),
]