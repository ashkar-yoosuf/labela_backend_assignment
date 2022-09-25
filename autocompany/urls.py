from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from users.views import ListUsers, CustomAuthToken, RegisterView
from autoparts import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view()),
    path('', include('autoparts.urls')),
    path('', include('carts.urls')),
    path('', include('orders.urls')),
    path('users/', user_views.ListUsers.as_view()),
    path('token/auth/', CustomAuthToken.as_view()),
]
