from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=CustomUserChangeForm
    model=CustomUser
    list_display=['raison_sociale', 'region', 'taille', 'anciennete', 'classe', 'contact', 'description', 'secteur_activite', 'statut', 'is_staff', 'is_active']
    list_filter=['is_staff', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)
