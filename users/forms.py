from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm._meta.fields + (
            'raison_sociale', 'region', 'taille', 'anciennete', 
            'contact', 'secteur_activite', 'statut', 'description'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Liste des champs de l'entreprise à rendre obligatoires
        champs_obligatoires = [
            'raison_sociale', 'region', 'taille', 'anciennete', 
            'contact', 'secteur_activite', 'statut', 'description'
        ]
        
        for champ in champs_obligatoires:
            if champ in self.fields:
                self.fields[champ].required = True
                
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