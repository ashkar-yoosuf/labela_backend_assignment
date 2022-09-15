from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from autoparts.models import Cart
from .forms import DeliveryForm


@login_required
def cartList(request, pk):

    if pk != request.user.id:
        raise PermissionDenied()

    else:
        context = {
            'cart': Cart.objects.filter(user_id=pk),
            'cart_id': Cart.objects.values_list('cart_id', flat=True).filter(user_id=pk).first()
            }
        return render(request, 'carts/details.html', context)


@login_required
def deliver(request, pk):

    if pk != request.user.id:
            raise PermissionDenied()

    else:
        if request.method == 'POST':
            form = DeliveryForm(request.POST)
            if form.is_valid():
                datetime = form.cleaned_data['datetime']
                context = {
                    'datetime': datetime,
                    'form': form
                }
                return render(request, 'carts/delivered.html', context)
        else:
            form = DeliveryForm()

        context = {
            'cart': Cart.objects.filter(user_id=pk),
            'cart_id': Cart.objects.values_list('cart_id', flat=True).filter(user_id=pk).first(),
            'form': form
        }
        
        return render(request, 'carts/details.html', context)
