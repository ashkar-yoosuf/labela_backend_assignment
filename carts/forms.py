from django import forms
from autoparts.models import Cart

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'

class DeliveryForm(forms.Form):
    datetime = forms.CharField(max_length=30)