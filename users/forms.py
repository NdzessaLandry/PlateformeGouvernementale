from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm._meta.fields + ('raison_sociale', 'region', 'taille', 'anciennete', 'contact', 'secteur_activite', 'statut', 'description')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class ChoixBesoinsForm(forms.Form):
    besoin_financement = forms.BooleanField(required=False, label="Besoin de financement")
    besoin_emballages = forms.BooleanField(required=False, label="Besoin d'emballages")
    besoin_transport = forms.BooleanField(required=False, label="Besoin de transport / logistique")
    besoin_appui_entreprise = forms.BooleanField(required=False, label="Besoin d'appui à l'entreprise")
    besoin_equipements = forms.BooleanField(required=False, label="Besoin d'équipements")
    besoin_intrants = forms.BooleanField(required=False, label="Besoin d'intrants")
    besoin_innovation_recherche = forms.BooleanField(required=False, label="Besoin d'innovation et recherche")