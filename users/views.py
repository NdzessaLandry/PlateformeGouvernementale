from django.shortcuts import render
from django.urls import reverse_lazy
import pandas as pd
import numpy as np
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ChoixBesoinsForm
from .models import reponseAuxBesoins, CustomUser, Classe
from brouillon.acm_tdc_projection import coordonnees_entreprises
from brouillon.prediction import predire_groupe_nouvel_individu

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


from django.shortcuts import render
from .models import CustomUser

@login_required(login_url='login')
def home_view(request):
    user = request.user
    context = {}

    # ================= CAS 1 : L'ENTREPRISE N'A PAS ENCORE DE CLASSE (FORMULAIRE) =================
    if user.classe is None:
        if request.method == 'POST':
            form = ChoixBesoinsForm(request.POST)
            if form.is_valid():
                # On formate les données de sortie pour ton algorithme
                besoins_dict = {
                    "besoin_financement": "Oui" if form.cleaned_data['besoin_financement'] else "Non",
                    "besoin_emballages": "Oui" if form.cleaned_data['besoin_emballages'] else "Non",
                    "besoin_transport": "Oui" if form.cleaned_data['besoin_transport'] else "Non",
                    "besoin_appui_entreprise": "Oui" if form.cleaned_data['besoin_appui_entreprise'] else "Non",
                    "besoin_equipements": "Oui" if form.cleaned_data['besoin_equipements'] else "Non",
                    "besoin_intrants": "Oui" if form.cleaned_data['besoin_intrants'] else "Non",
                    "besoin_innovation_recherche": "Oui" if form.cleaned_data['besoin_innovation_recherche'] else "Non"
                }
                besoins_dict["region"] = user.region.libele if user.region else "Non renseigné"
                besoins_dict["statut_juridique"] = user.statut.libele if user.statut else "Non renseigné"
                besoins_dict["secteur_activite_princ"] = user.secteur_activite.libele if user.secteur_activite else "Non renseigné"
                besoins_dict["taille_entreprise"] = user.taille.libele if user.taille else "Non renseigné"
                besoins_dict["date_debut_activite"] = user.anciennete.libele if user.anciennete else "Non renseigné"

            
                # --- APPEL DE TON ALGORITHME ---
                # Exemple : nouvelle_classe = ton_algorithme_de_classification(besoins_dict)
                # (Assure-toi que ton algorithme retourne une instance du modèle 'Classe')
                classe = predire_groupe_nouvel_individu(coordonnees_entreprises(besoins_dict))["classe_predite"]
                classe_attribuee = Classe.objects.get(libele=classe)
                user.classe = classe_attribuee
                
                user.save() # On met à jour l'utilisateur en BDD
                return redirect('home') # On recharge proprement la page en mode GET
        else:
            form = ChoixBesoinsForm()
            
        context['form_besoins'] = form
        context['a_besoin_de_classe'] = True

    # ================= CAS 2 : L'ENTREPRISE A UNE CLASSE (RECOMMANDATIONS SUR MESURE) =================
    else:
        context['a_besoin_de_classe'] = False
        
        # On va chercher dans la table reponseAuxBesoins les entreprises liées à la classe de l'utilisateur
        liaisons = reponseAuxBesoins.objects.filter(classe=user.classe).select_related('entreprise')
        
        # On extrait la liste des entreprises cibles
        entreprises_susceptibles_aider = [liaison.entreprise for liaison in liaisons]
        
        context['entreprises_recommandees'] = entreprises_susceptibles_aider

    return render(request, 'home.html', context)