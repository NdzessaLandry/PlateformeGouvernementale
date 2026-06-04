from django.shortcuts import render
from django.urls import reverse_lazy
import pandas as pd
import numpy as np
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def classement(listeParametre):
    valeursPropres=pd.read_csv("data/mca_eigenvalues.csv")
    coord_modalites=pd.read_csv("data/mca_coordinates.csv")
    if len(listeParametre)==5:
        print("OK")
    else:
        print('OK')
