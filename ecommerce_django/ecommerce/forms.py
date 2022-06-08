from tkinter import Widget
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Prodotti
from .models import Recensioni
from .models import Vendite
from .models import RecensoniFornitori
from crispy_forms.helper import FormHelper

#form di creazione utente
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#form di creazione del prodotto
class ProductForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False 

    class Meta:
        model = Prodotti
        fields = ['immagine', 'titolo', 'scheda_tecnica', 'categoria', 'quantità', 'prezzo']

        widget = {
            'immagine': forms.FileInput(attrs={'class': 'form-control'}),
            'titolo': forms.TextInput(attrs={'class': 'form-control'}),
            'scheda_tecnica': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'quantità': forms.TextInput(attrs={'class': 'form-control'}),
            'prezzo': forms.TextInput(attrs={'class': 'form-control'}),
        }

#form di creazione recensione del prodotto
class RecensioniForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False 

    class Meta:
        model = Recensioni
        fields = ['descrizione', 'stelle']

        widget = {
            'descrizione': forms.TextInput(attrs={'class': 'form-control'}),
            'stelle': forms.TextInput(attrs={'class': 'form-control'}),
        }

#form della vendita
class VenditaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False 

    class Meta:
        model = Vendite
        fields = ['quantità']

        widget = {
            'quantità': forms.TextInput(attrs={'class': 'form-control'}),
        }

#form di creazione recensione di un fornitore
class RecensioniFornitoreForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False 

    class Meta:
        model = RecensoniFornitori
        fields = ['recensione', 'stelle']

        widget = {
            'recensione': forms.TextInput(attrs={'class': 'form-control'}),
            'stelle': forms.TextInput(attrs={'class': 'form-control'}),
        }

#form di ricerca per prezzo
class MyCheckBox(forms.Form):
    prezzo = forms.BooleanField(required=False)
