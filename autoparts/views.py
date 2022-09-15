from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from .models import Product, Cart
from .forms import ProductForm, QuantityForm
from carts.forms import CartForm


class ProductListView(ListView):
    model = Product
    template_name = 'autoparts/details.html'
    context_object_name = 'products'
    ordering = ['name']


@login_required
def detail(request, pk):

    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            product_name = Product.objects.values_list('name', flat=True).filter(id=pk).first()
            cart = Cart(user_id=request.user, cart_id=request.user.id+5, product_id=pk, product_name=product_name, quantity=quantity)
            cart.save()
            return redirect('product-detail', pk)
    else:
        form = QuantityForm()
    
    context = {
        'products': Product.objects.all(),
        'id' : pk,
        'form': form
    }
    
    return render(request, 'autoparts/product_detail.html', context)


@login_required
def delete(request, pk, cart_id):

    if Cart.objects.filter(cart_id=request.user.id+5).values_list('user_id', flat=True).first() != request.user.id:
        raise PermissionDenied()

    else:
        cart = Cart.objects.filter(user_id=request.user.id)
        product = cart.get(product_id=pk)
        cart_id = cart.values_list('cart_id', flat=True).filter(product_id=pk).first()
        product.delete()

        context = {
            'cart': cart,
            'cart_id': cart_id
        }

        return render(request, 'carts/details.html', context)
    