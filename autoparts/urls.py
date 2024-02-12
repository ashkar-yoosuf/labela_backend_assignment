from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.ListProducts.as_view()),
    path('home/<int:pk>/detail/', views.ProductDetail.as_view(), name='product-detail'),
]