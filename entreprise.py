import os
import django
    
    # Configuration de l'environnement Django pour script autonome
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper_project.settings')
django.setup()

from django.contrib.auth.hashers import make_password

# Importation du nouveau modèle
from users.models import (
    CustomUser, Region, Taille, Anciennete,
    SecteurActivite, Statut, Classe, reponseAuxBesoins
)

# ─────────────────────────────────────────────────────────────────────────────
# 0. HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_or_warn(model, **kwargs):
    """Retourne l'objet ou None avec un avertissement si absent."""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        print(f"[AVERTISSEMENT] {model.__name__} introuvable : {kwargs}")
        return None

def creer_entreprise(data: dict) -> None:
    """Crée un CustomUser-entreprise et l'associe à reponseAuxBesoins."""
    if CustomUser.objects.filter(raison_sociale=data['raison_sociale']).exists():
        print(f"[IGNORÉ] Déjà en base : {data['raison_sociale']}")
        return

    # Remplacement de 'nom' par 'libele' d'après les choix de votre modèle
    region          = get_or_warn(Region,         libele=data['region'])
    taille          = get_or_warn(Taille,         libele=data['taille'])
    anciennete      = get_or_warn(Anciennete,     libele=data['anciennete'])
    secteur_activite= get_or_warn(SecteurActivite,libele=data['secteur_activite'])
    statut          = get_or_warn(Statut,         libele=data['statut'])
    
    # Si pour le modèle Classe vous utilisez aussi un champ textuel ou 'nom', adaptez-le. 
    # Si c'est le champ par défaut 'nom' ou 'libele', ajustez ici :
    classe          = get_or_warn(Classe,         libele=data['classe']) 

    user = CustomUser(
        username         = data['username'],
        password         = make_password('BusinessPartner2025!'),
        raison_sociale   = data['raison_sociale'],
        contact          = data['contact'],
        description      = data['description'],
        region           = region,
        taille           = taille,
        anciennete       = anciennete,
        secteur_activite = secteur_activite,
        statut           = statut,
        classe           = classe,
        is_active        = True,
    )
    user.save()
    print(f"[OK] Entreprise créée : {data['raison_sociale']}")

    if classe is not None:
        try:
            besoin, created = reponseAuxBesoins.objects.get_or_create(
                entreprise=user,
                classe=classe
            )
            if created:
                print(f"[OK] Relation créée dans reponseAuxBesoins pour {data['raison_sociale']} (Classe {classe.libele})")
        except Exception as e:
            print(f"[ERREUR] Impossible de lier l'entreprise au besoin : {e}")

# ─────────────────────────────────────────────────────────────────────────────
# 1. DONNÉES — CLASSE 1 , 2 et 3
# ─────────────────────────────────────────────────────────────────────────────
# (Vos listes CLASSE_1, CLASSE_2, CLASSE_3 restent inchangées ici...)

# ─────────────────────────────────────────────────────────────────────────────
# 4. SCRIPT D'ÉXÉCUTION (À ajouter à la fin du fichier)
# ─────────────────────────────────────────────────────────────────────────────

def executer_importation():
    """Parcourt toutes les listes et lance l'intégration."""
    print("--- Début de l'importation de la Classe 1 ---")
    for ent in CLASSE_1:
        creer_entreprise(ent)
        
    print("\n--- Début de l'importation de la Classe 2 ---")
    for ent in CLASSE_2:
        creer_entreprise(ent)
        
    print("\n--- Début de l'importation de la Classe 3 ---")
    # Note : Vérifiez que votre liste CLASSE_3 est bien fermée dans votre code complet
    for ent in CLASSE_3:
        creer_entreprise(ent)

# ─────────────────────────────────────────────────────────────────────────────
# 1. DONNÉES — CLASSE 1
# ─────────────────────────────────────────────────────────────────────────────

CLASSE_1 = [
    {
        'username'         : 'adsk',
        'raison_sociale'   : 'ADSK SARL',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 a 9 ans',
        'contact'          : '+237 699 45 12 78 | contact@adsk-cameroun.cm',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "ADSK SARL est une entreprise camerounaise spécialisée dans la "
            "transformation des produits agricoles locaux et dans la création "
            "d'une centrale d'achat de produits Made in Cameroon. Elle accompagne "
            "les petites structures agro-productives en leur offrant des débouchés "
            "commerciaux fiables et en valorisant les productions locales sur le "
            "marché national et sous-régional. Ses activités couvrent la collecte, "
            "le conditionnement et la distribution de produits agricoles transformés."
        ),
    },
    {
        'username'         : 'agid_cameroun',
        'raison_sociale'   : 'AGID-Cameroun SARL',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '10 a 19 ans',
        'contact'          : '+237 677 23 45 90 | info@agid-cameroun.cm',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "AGID-Cameroun SARL est un acteur de référence dans la distribution "
            "d'intrants agricoles et la transformation agroalimentaire au Cameroun. "
            "Elle produit des jus et pâtes à base de fruits et légumes locaux, "
            "et distribue des semences potagères, des fertilisants organiques et "
            "des équipements de transformation aux agriculteurs et petites unités "
            "de production. Partenaire privilégié des entreprises ayant des besoins "
            "en intrants, équipements et conseil technique agricole."
        ),
    },
    {
        'username'         : 'sodecoton',
        'raison_sociale'   : 'SODECOTON',
        'region'           : 'Nord',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+237 222 27 10 20 | direction@sodecoton.cm',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "La Société de Développement du Coton (SODECOTON) est le principal "
            "opérateur de la filière cotonnière camerounaise depuis 1974. Elle "
            "emploie directement 2 000 personnes et soutient plus de 200 000 "
            "agriculteurs à travers la fourniture de semences améliorées, "
            "d'engrais subventionnés et de formations techniques. Avec une "
            "production de 300 000 tonnes de coton-graine en 2023, elle constitue "
            "un partenaire stratégique incontournable pour toute entreprise du "
            "secteur agricole des régions Nord et Extrême-Nord du Cameroun."
        ),
    },
    {
        'username'         : 'atlas_holding',
        'raison_sociale'   : 'Atlas Holding',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 a 9 ans',
        'contact'          : '+237 691 78 34 56 | contact@atlasholding.cm',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "Atlas Holding est une société camerounaise spécialisée dans la "
            "production et la transformation de farines et dérivés à base de "
            "produits locaux tels que la patate douce, l'igname, le manioc et "
            "la banane plantain. Elle développe des produits biologiques "
            "valorisant la culture alimentaire africaine, destinés au marché "
            "national, sous-régional et international. Elle offre aux petites "
            "entreprises agricoles des opportunités de valorisation de leurs "
            "productions grâce à des circuits d'approvisionnement locaux."
        ),
    },
    {
        'username'         : 'stm_manioc',
        'raison_sociale'   : 'STM (Société de Transformation du Manioc)',
        'region'           : 'Littoral',
        'taille'           : 'Très Petite Entreprise',
        'anciennete'       : '5 a 9 ans',
        'contact'          : '+237 655 12 89 03 | stm.manioc@gmail.com',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "La Société de Transformation du Manioc (STM), créée en 2016, est "
            "spécialisée dans la transformation semi-industrialelle du manioc en "
            "amidon à usage industriel. Elle entretient un réseau direct de plus "
            "de 100 petits producteurs de manioc qu'elle accompagne techniquement "
            "et qu'elle approvisionne en intrants. Avec l'ambition de devenir "
            "l'acteur de référence dans la production d'amidon de manioc dans "
            "la zone CEMAC, STM offre un débouché stable et valorisant pour "
            "les producteurs de tubercules de la région du Littoral."
        ),
    },
    {
        'username'         : 'agl_cameroun',
        'raison_sociale'   : 'AGL Cameroun (Africa Global Logistics)',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+237 233 42 76 76 | cameroun@aglgroup.com',
        'secteur_activite' : 'Transport et logistique',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "AGL Cameroun (Africa Global Logistics) est l'acteur majeur du "
            "transport et de la logistique en Afrique centrale, certifié ISO 9001, "
            "ISO 14001, ISO 45001 et Ecovadis. Avec 3 100 employés répartis sur "
            "12 sites à travers le Cameroun, elle propose une offre complète de "
            "services logistiques : transit, entreposage, distribution, gestion "
            "de la chaîne d'approvisionnement et solutions de transport multimodal. "
            "Elle accompagne les entreprises agricoles et agroalimentaires dans "
            "l'acheminement de leurs produits vers les marchés nationaux et régionaux."
        ),
    },
    {
        'username'         : 'nfbank',
        'raison_sociale'   : 'National Financial Bank (NFBank)',
        'region'           : 'Centre',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+237 222 22 10 60 | contact@nfbank.cm',
        'secteur_activite' : 'Services financiers et bancaires',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "La National Financial Bank (NFBank) est une banque universelle "
            "camerounaise disposant d'un réseau d'agences couvrant l'ensemble "
            "du territoire national. Sélectionnée par le MINEPAT dans le cadre "
            "du programme de soutien au secteur privé en partenariat avec le PNUD "
            "(novembre 2024), elle met à disposition des TPE et PME des lignes de "
            "crédit à taux bonifiés pour financer leurs projets d'investissement "
            "et leur fonds de roulement. Également implantée auprès du secteur agricole."
        ),
    },
    {
        'username'         : 'john_deere_cm',
        'raison_sociale'   : 'John Deere',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+1 309 765 8000 | africa.distributors@johndeere.com',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "John Deere est le leader mondial de la fabrication de machines "
            "agricoles et d'équipements de travaux publics, fondé en 1837 aux "
            "États-Unis. La marque propose une gamme complète d'équipements — "
            "tracteurs, moissonneuses-batteuses, systèmes d'irrigation, outils "
            "de précision — adaptée aux différentes cultures et conditions "
            "climatiques, avec une présence croissante en Afrique centrale via "
            "un réseau de distributeurs agréés au Cameroun. Partenaire "
            "technologique de référence pour la mécanisation et la modernisation."
        ),
    },
    {
        'username'         : 'tetra_pak_cm',
        'raison_sociale'   : 'Tetra Pak',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+27 11 667 2000 | info.africa@tetrapak.com',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "Tetra Pak est le leader mondial des solutions de transformation et "
            "d'emballage alimentaire, fondé en 1951 en Suède. La société propose "
            "des systèmes de production avancés pour la transformation du lait, "
            "des jus, des soupes et des aliments liquides, accompagnés d'un réseau "
            "international de fournisseurs d'ingrédients et de services techniques. "
            "Ses solutions modulaires, adaptables aux capacités d'investissement."
        ),
    },
    {
        'username'         : 'buhler_group_cm',
        'raison_sociale'   : 'Bühler Group',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+27 11 801 0000 | africa@buhlergroup.com',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "Bühler Group est le spécialiste mondial des équipements de "
            "transformation des céréales, du riz, du cacao, du café et des "
            "aliments pour animaux, fondé en 1860 en Suisse. Ses solutions "
            "modulaires et évolutives sont particulièrement adaptées aux "
            "capacités d'investissement des petites et moyennes unités de "
            "transformation agroalimentaire africaines. Conception et maintenance."
        ),
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 2. DONNÉES — CLASSE 2 : LES OPÉRATEURS FINANCIERS ET SERVICES ÉTABLIS
# ─────────────────────────────────────────────────────────────────────────────

CLASSE_2 = [
    {
        'username'         : 'cac_audit',
        'raison_sociale'   : 'Cameroun Audit Conseil (CAC)',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+237 233 40 02 23 | contact@cac-audit.cm',
        'secteur_activite' : 'Services professionnels (consulting, comptabilite, etc.)',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Cameroun Audit Conseil (CAC) est l'un des plus grands cabinets "
            "d'audit et de conseil en Afrique subsaharienne, basé à Douala. "
            "Ses équipes pluridisciplinaires accompagnent les entreprises et "
            "institutions financières dans leur développement et leur expansion "
            "grâce à des solutions innovantes en audit légal et contractuel."
        ),
    },
    {
        'username'         : 'cfair_group',
        'raison_sociale'   : 'Groupe CFAIR',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 a 9 ans',
        'contact'          : '+237 690 34 56 78 | contact@cfair.cm',
        'secteur_activite' : 'Services professionnels (consulting, comptabilite, etc.)',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Le Groupe CFAIR est un cabinet camerounais de conseil et de services "
            "aux entreprises spécialisé dans l'ingénierie informatique, la "
            "comptabilité, les déclarations fiscales, le conseil en gestion "
            "financière et l'accompagnement lors des audits. Il organise "
            "régulièrement des ateliers et séminaires pour entrepreneurs."
        ),
    },
    {
        'username'         : 'gms_consulting',
        'raison_sociale'   : 'GMS Consulting Group',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '10 a 19 ans',
        'contact'          : '+237 677 89 01 23 | gms@geconsultingcm.com',
        'secteur_activite' : 'Services professionnels (consulting, comptabilite, etc.)',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "GMS Consulting Group est un cabinet camerounais de conseil en "
            "management et en développement organisationnel, présent à Douala "
            "et à Yaoundé. Il propose une offre intégrée de services incluant "
            "le marketing digital, l'ingénierie-conseil, l'audit interne, "
            "la certification ISO (9001, 14001, 45001) et la gestion de projets."
        ),
    },
    {
        'username'         : 'experts_mac',
        'raison_sociale'   : 'Experts-Mac',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '10 a 19 ans',
        'contact'          : '+237 651 07 81 46 | clarisse.njike@experts-mac.net',
        'secteur_activite' : 'Services professionnels (consulting, comptabilite, etc.)',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Experts-Mac est un cabinet d'audit, comptable et juridique basé "
            "à Douala, titulaire d'un agrément communautaire pour l'exercice "
            "de la profession d'Expert-Comptable. Il propose des services de "
            "conseil en banque africaine, fiscalité, implémentation ERP SAP, "
            "audit légal et contractuel, commissariat aux comptes."
        ),
    },
    {
        'username'         : 'bgfibank_cm',
        'raison_sociale'   : 'BGFIBank Cameroun',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+237 233 43 23 00 | contact@bgfibank.cm',
        'secteur_activite' : 'Services financiers et bancaires',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "BGFIBank Cameroun est la filiale camerounaise du groupe bancaire "
            "panafricain gabonais BGFI. Institution financière de référence "
            "au Cameroun, elle accompagne les entreprises dans leurs besoins "
            "de financement structuré, de trésorerie, de commerce international."
        ),
    },
    {
        'username'         : 'sap_cm',
        'raison_sociale'   : 'SAP SE',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+27 11 235 6000 | africa.info@sap.com',
        'secteur_activite' : 'Technologies de l information et de la communication (TIC)',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "SAP SE est le leader mondial des logiciels de gestion d'entreprise "
            "(ERP), fondé en 1972 en Allemagne. Ses solutions couvrent l'ensemble "
            "des processus métiers — finance, logistique, ressources humaines, "
            "achats, ventes, production — et sont déployées au Cameroun."
        ),
    },
    {
        'username'         : 'odoo_cm',
        'raison_sociale'   : 'Odoo S.A.',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '10 a 19 ans',
        'contact'          : '+32 81 25 09 00 | partners.africa@odoo.com',
        'secteur_activite' : 'Technologies de l information et de la communication (TIC)',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Odoo est une suite intégrée d'applications de gestion d'entreprise "
            "open source, développée en Belgique depuis 2005. Reconnue comme "
            "l'alternative ERP la plus accessible aux entreprises africaines de "
            "taille intermédiaire, elle couvre la comptabilité, les ventes, les achats."
        ),
    },
    {
        'username'         : 'webgram_cm',
        'raison_sociale'   : 'WEBGRAM',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 a 9 ans',
        'contact'          : '+221 77 123 45 67 | contact@agencewebgram.com',
        'secteur_activite' : 'Technologies de l information et de la communication (TIC)',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "WEBGRAM est une agence africaine de développement d'applications "
            "web, mobiles et de solutions ERP fondée au Sénégal et présente "
            "dans 15 pays africains dont le Cameroun. Sa solution phare SmartERP "
            "est déjà déployée chez des entreprises camerounaises."
        ),
    },
    {
        'username'         : 'safir_consulting',
        'raison_sociale'   : 'Safir Consulting',
        'region'           : 'Centre',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '10 a 19 ans',
        'contact'          : '+33 1 84 60 12 34 | contact@safir-consulting.fr',
        'secteur_activite' : 'Services professionnels (consulting, comptabilite, etc.)',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Safir Consulting est un cabinet de conseil en management et "
            "systèmes d'information fondé en France en 2014, spécialisé dans "
            "les secteurs de la banque, de la finance et de l'assurance. Il "
            "accompagne les institutions financières africaines."
        ),
    },
    {
        'username'         : 'bc_pme',
        'raison_sociale'   : 'Banque Camerounaise des PME (BC-PME)',
        'region'           : 'Centre',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '5 a 9 ans',
        'contact'          : '+237 222 70 00 00 | info@bcpme.cm',
        'secteur_activite' : 'Services financiers et bancaires',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "La Banque Camerounaise des Petites et Moyennes Entreprises "
            "(BC-PME) est l'institution publique spécifiquement dédiée au "
            "financement des PME camerounaises. Elle propose une gamme de "
            "produits financiers adaptés aux structures de taille intermédiaire."
        ),
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 3. DONNÉES — CLASSE 3 : LES PETITES ENTREPRISES MULTI-SECTORIELLES
# ─────────────────────────────────────────────────────────────────────────────

CLASSE_3 = [
    {
        'username'         : 'fabrik_aliments',
        'raison_sociale'   : 'Fabrik Aliments',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 a 9 ans',
        'contact'          : '+237 690 12 34 56 | contact@fabrikaliments.com',
        'secteur_activite' : 'Services professionnels (consulting, comptabilite, etc.)',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "Fabrik Aliments est le pionnier camerounais du conseil et de "
            "la formation en agroalimentaire en Afrique centrale. La structure "
            "propose aux petites entreprises agroalimentaires un annuaire de "
            "fournisseurs d'ingrédients et d'équipements, des services."
        ),
    },
    {
        'username'         : 'nofia_cm',
        'raison_sociale'   : "Nouvelle Financière d'Afrique (NOFIA)",
        'region'           : 'Centre',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 a 9 ans',
        'contact'          : '+237 699 78 90 12 | nofia.microfinance@gmail.com',
        'secteur_activite' : 'Services financiers et bancaires',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "La Nouvelle Financière d'Afrique (NOFIA) est un établissement de "
            "microfinance camerounais sélectionné par le MINEPAT dans le cadre "
            "du programme de soutien au secteur privé en partenariat avec le "
            "PNUD (novembre 2024). Elle propose aux TPE et PME des lignes de crédit."
        ),
    },
    {
        'username'         : 'focep_cm',
        'raison_sociale'   : "Fonds Camerounais d'Épargne pour le Progrès (FOCEP)",
        'region'           : 'Centre',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '10 a 19 ans',
        'contact'          : '+237 222 30 45 67 | focep@microfinance-cm.com',
        'secteur_activite' : 'Services financiers et bancaires',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "Le Fonds Camerounais d'Épargne pour le Progrès (FOCEP) est un "
            "établissement de microfinance agréé par la COBAC, sélectionné "
            "par le MINEPAT et le PNUD pour le programme de soutien au secteur "
            "privé de 2024. Il propose aux entreprises en développement des produits."
        ),
    },
    {
        'username'         : 'scr_cameroun',
        'raison_sociale'   : 'Société Camerounaise de Raffinage (SCR)',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+237 233 37 00 00 | contact@scr-cameroun.cm',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "La Société Camerounaise de Raffinage (SCR), implantée dans la "
            "Zone Industrielle de Bassa à Douala, est spécialisée dans la "
            "transformation des fruits du palmier à huile en huile végétale "
            "comestible raffinée, en savons et en margarines."
        ),
    },
    {
        'username'         : 'cameroon_tea',
        'raison_sociale'   : 'Cameroon Tea Estates (CTE)',
        'region'           : 'Ouest',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '20 ans et plus',
        'contact'          : '+237 233 45 10 00 | cte@cameroon-tea.cm',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "Cameroon Tea Estates (CTE) est un acteur majeur spécialisé dans la "
            "production, le conditionnement, la récolte et la distribution du "
            "thé de haute qualité sur l'ensemble du territoire camerounais."
        ),
    },
]
# ─────────────────────────────────────────────────────────────────────────────
# 4. EXÉCUTION
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
   
    # Lancement de l'importation
    executer_importation()