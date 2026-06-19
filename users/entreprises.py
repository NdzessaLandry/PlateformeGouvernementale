from django.contrib.auth.hashers import make_password

# Importation du nouveau modèle
from models import (
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

    region          = get_or_warn(Region,         nom=data['region'])
    taille          = get_or_warn(Taille,         nom=data['taille'])
    anciennete      = get_or_warn(Anciennete,     nom=data['anciennete'])
    secteur_activite= get_or_warn(SecteurActivite,nom=data['secteur_activite'])
    statut          = get_or_warn(Statut,         nom=data['statut'])
    classe          = get_or_warn(Classe,         nom=data['classe'])

    # 1. Création de l'utilisateur / entreprise
    user = CustomUser(
        username         = data['username'],
        email            = data['email'],
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

    # 2. Ajout automatique dans la table reponseAuxBesoins si la classe existe
    if classe is not None:
        try:
            besoin, created = reponseAuxBesoins.objects.get_or_create(
                entreprise=user,
                classe=classe
            )
            if created:
                print(f"[OK] Relation créée dans reponseAuxBesoins pour {data['raison_sociale']} (Classe {classe.nom})")
        except Exception as e:
            print(f"[ERREUR] Impossible de lier l'entreprise au besoin : {e}")
    else:
        print(f"[INFO] Relation non créée pour {data['raison_sociale']} car la Classe est introuvable.")


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
# 1. DONNÉES — CLASSE 1 : LES ACTEURS AGRO-PRODUCTIFS ÉMERGENTS
# ─────────────────────────────────────────────────────────────────────────────

CLASSE_1 = [

    {
        'username'         : 'adsk',
        'raison_sociale'   : 'ADSK SARL',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 à 9 ans',
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
        'anciennete'       : '10 à 19 ans',
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
        'anciennete'       : 'Plus de 20 ans',
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
        'anciennete'       : '5 à 9 ans',
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
        'anciennete'       : '5 à 9 ans',
        'contact'          : '+237 655 12 89 03 | stm.manioc@gmail.com',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "La Société de Transformation du Manioc (STM), créée en 2016, est "
            "spécialisée dans la transformation semi-industrielle du manioc en "
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
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+237 233 42 76 76 | cameroun@aglgroup.com',
        'secteur_activite' : 'Transport et Logistique',
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
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+237 222 22 10 60 | contact@nfbank.cm',
        'secteur_activite' : 'Services Financiers et Bancaires',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "La National Financial Bank (NFBank) est une banque universelle "
            "camerounaise disposant d'un réseau d'agences couvrant l'ensemble "
            "du territoire national. Sélectionnée par le MINEPAT dans le cadre "
            "du programme de soutien au secteur privé en partenariat avec le PNUD "
            "(novembre 2024), elle met à disposition des TPE et PME des lignes de "
            "crédit à taux bonifiés pour financer leurs projets d'investissement "
            "et leur fonds de roulement. Elle propose également des produits "
            "d'épargne, des solutions de paiement mobile et un accompagnement "
            "personnalisé aux jeunes entrepreneurs du secteur agricole."
        ),
    },

    {
        'username'         : 'john_deere_cm',
        'raison_sociale'   : 'John Deere',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+1 309 765 8000 | africa.distributors@johndeere.com',
        'secteur_activite' : 'Fabrication de Machines et Équipements Agricoles',
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
            "technologique de référence pour la mécanisation et la modernisation "
            "des exploitations agricoles camerounaises de toutes tailles."
        ),
    },

    {
        'username'         : 'tetra_pak_cm',
        'raison_sociale'   : 'Tetra Pak',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+27 11 667 2000 | info.africa@tetrapak.com',
        'secteur_activite' : 'Équipements et Emballages Agroalimentaires',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "Tetra Pak est le leader mondial des solutions de transformation et "
            "d'emballage alimentaire, fondé en 1951 en Suède. La société propose "
            "des systèmes de production avancés pour la transformation du lait, "
            "des jus, des soupes et des aliments liquides, accompagnés d'un réseau "
            "international de fournisseurs d'ingrédients et de services techniques. "
            "Ses solutions modulaires, adaptables aux capacités d'investissement "
            "des unités de taille moyenne, permettent aux entreprises "
            "agroalimentaires camerounaises de moderniser leur outil de production "
            "et d'accéder aux standards d'hygiène requis pour l'exportation."
        ),
    },

    {
        'username'         : 'buhler_group_cm',
        'raison_sociale'   : 'Bühler Group',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+27 11 801 0000 | africa@buhlergroup.com',
        'secteur_activite' : 'Équipements de Transformation des Céréales et Aliments',
        'statut'           : 'SARL',
        'classe'           : '1',
        'description'      : (
            "Bühler Group est le spécialiste mondial des équipements de "
            "transformation des céréales, du riz, du cacao, du café et des "
            "aliments pour animaux, fondé en 1860 en Suisse. Ses solutions "
            "modulaires et évolutives sont particulièrement adaptées aux "
            "capacités d'investissement des petites et moyennes unités de "
            "transformation agroalimentaire africaines. Avec des bureaux "
            "régionaux à Johannesburg et Lagos, Bühler accompagne les "
            "entrepreneurs africains dans la conception, l'installation et "
            "la maintenance de leurs équipements de transformation, contribuant "
            "à la création de valeur ajoutée locale dans la filière céréalière."
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
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+237 233 40 02 23 | contact@cac-audit.cm',
        'secteur_activite' : 'Audit, Conseil et Expertise Comptable',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Cameroun Audit Conseil (CAC) est l'un des plus grands cabinets "
            "d'audit et de conseil en Afrique subsaharienne, basé à Douala. "
            "Ses équipes pluridisciplinaires accompagnent les entreprises et "
            "institutions financières dans leur développement et leur expansion "
            "grâce à des solutions innovantes en audit légal et contractuel, "
            "expertise comptable, conseil fiscal, conseil en management, "
            "restructuration et due diligence. Reconnu au plan international "
            "pour la qualité de ses travaux, CAC est le partenaire de référence "
            "pour les entreprises souhaitant structurer leur gouvernance et "
            "renforcer leur crédibilité financière."
        ),
    },

    {
        'username'         : 'cfair_group',
        'raison_sociale'   : 'Groupe CFAIR',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 à 9 ans',
        'contact'          : '+237 690 34 56 78 | contact@cfair.cm',
        'secteur_activite' : 'Conseil IT, Comptabilité et Formation',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Le Groupe CFAIR est un cabinet camerounais de conseil et de services "
            "aux entreprises spécialisé dans l'ingénierie informatique, la "
            "comptabilité, les déclarations fiscales, le conseil en gestion "
            "financière et l'accompagnement lors des audits. Il organise "
            "régulièrement des ateliers et séminaires pour sensibiliser les "
            "entrepreneurs camerounais aux enjeux financiers et numériques. "
            "Son approche personnalisée et sa maîtrise de l'environnement "
            "réglementaire camerounais en font un partenaire de choix pour "
            "les PME souhaitant optimiser leur gestion et moderniser leurs "
            "systèmes d'information."
        ),
    },

    {
        'username'         : 'gms_consulting',
        'raison_sociale'   : 'GMS Consulting Group',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '10 à 19 ans',
        'contact'          : '+237 677 89 01 23 | gms@geconsultingcm.com',
        'secteur_activite' : 'Conseil en Management et Formation',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "GMS Consulting Group est un cabinet camerounais de conseil en "
            "management et en développement organisationnel, présent à Douala "
            "et à Yaoundé. Il propose une offre intégrée de services incluant "
            "le marketing digital, l'ingénierie-conseil, l'audit interne, "
            "la certification ISO (9001, 14001, 45001), le management de "
            "projets, la gestion des ressources humaines et la formation "
            "professionnelle. GMS Consulting Group accompagne les entreprises "
            "établies dans le renforcement de leurs capacités managériales, "
            "l'amélioration de leurs processus internes et leur mise en "
            "conformité avec les standards internationaux de qualité."
        ),
    },

    {
        'username'         : 'experts_mac',
        'raison_sociale'   : 'Experts-Mac',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '10 à 19 ans',
        'contact'          : '+237 651 07 81 46 | clarisse.njike@experts-mac.net',
        'secteur_activite' : 'Audit, Conseil IT et Fiscalité',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Experts-Mac est un cabinet d'audit, comptable et juridique basé "
            "à Douala, titulaire d'un agrément communautaire pour l'exercice "
            "de la profession d'Expert-Comptable. Il propose des services de "
            "conseil en banque africaine, fiscalité, implémentation ERP SAP, "
            "audit légal et contractuel, commissariat aux comptes, gestion "
            "de la paie et des charges sociales, gestion des ressources "
            "humaines, management de projets et partenariat public-privé. "
            "Son expertise combinant finance, droit et technologie en fait "
            "un interlocuteur de référence pour les entreprises de services "
            "financiers souhaitant moderniser leur système de gestion."
        ),
    },

    {
        'username'         : 'bgfibank_cm',
        'raison_sociale'   : 'BGFIBank Cameroun',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+237 233 43 23 00 | contact@bgfibank.cm',
        'secteur_activite' : 'Services Financiers et Bancaires',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "BGFIBank Cameroun est la filiale camerounaise du groupe bancaire "
            "panafricain gabonais BGFI. Institution financière de référence "
            "au Cameroun, elle accompagne les entreprises dans leurs besoins "
            "de financement structuré, de trésorerie, de commerce international "
            "et de gestion de patrimoine. Elle a notamment mis à disposition "
            "des PME une ligne de financement de 10 milliards de FCFA dans "
            "le cadre du soutien post-Covid. Reconnue pour la solidité de son "
            "bilan et la qualité de son service client orienté corporate, "
            "elle est le partenaire financier stratégique des entreprises "
            "établies en quête de financements structurés."
        ),
    },

    {
        'username'         : 'sap_cm',
        'raison_sociale'   : 'SAP SE',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+27 11 235 6000 | africa.info@sap.com',
        'secteur_activite' : 'Logiciels ERP et Technologies de l\'Information',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "SAP SE est le leader mondial des logiciels de gestion d'entreprise "
            "(ERP), fondé en 1972 en Allemagne. Ses solutions couvrent l'ensemble "
            "des processus métiers — finance, logistique, ressources humaines, "
            "achats, ventes, production — et sont déployées par des partenaires "
            "certifiés présents au Cameroun et dans la sous-région. SAP propose "
            "des éditions adaptées aux PME (SAP Business One, SAP S/4HANA Cloud) "
            "permettant une digitalisation progressive et abordable des opérations "
            "des entreprises de services financiers souhaitant moderniser leur "
            "système d'information et améliorer leur pilotage de performance."
        ),
    },

    {
        'username'         : 'odoo_cm',
        'raison_sociale'   : 'Odoo S.A.',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '10 à 19 ans',
        'contact'          : '+32 81 25 09 00 | partners.africa@odoo.com',
        'secteur_activite' : 'Logiciels ERP Open Source',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Odoo est une suite intégrée d'applications de gestion d'entreprise "
            "open source, développée en Belgique depuis 2005. Reconnue comme "
            "l'alternative ERP la plus accessible aux entreprises africaines de "
            "taille intermédiaire, elle couvre la comptabilité, les ventes, les "
            "achats, la gestion de stock, le CRM, la RH, le e-commerce et bien "
            "d'autres modules configurables selon les réglementations locales. "
            "Des partenaires certifiés Odoo au Cameroun assurent l'implémentation, "
            "la formation et la maintenance des solutions. Son modèle open source "
            "et ses coûts de déploiement réduits en font une option privilégiée "
            "pour les entreprises souhaitant digitaliser leur gestion sans "
            "investissement initial prohibitif."
        ),
    },

    {
        'username'         : 'webgram_cm',
        'raison_sociale'   : 'WEBGRAM',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 à 9 ans',
        'contact'          : '+221 77 123 45 67 | contact@agencewebgram.com',
        'secteur_activite' : 'Développement Logiciel et ERP',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "WEBGRAM est une agence africaine de développement d'applications "
            "web, mobiles et de solutions ERP fondée au Sénégal et présente "
            "dans 15 pays africains dont le Cameroun. Sa solution phare SmartERP "
            "est déjà déployée chez des entreprises camerounaises et propose "
            "des modules configurables selon les réglementations locales : "
            "comptabilité OHADA, gestion commerciale, paie, RH, production "
            "et logistique. WEBGRAM accompagne les entreprises dans leur "
            "transformation digitale avec des solutions sur mesure adaptées "
            "aux réalités économiques, juridiques et fiscales africaines, "
            "avec un support local réactif et une tarification accessible."
        ),
    },

    {
        'username'         : 'safir_consulting',
        'raison_sociale'   : 'Safir Consulting',
        'region'           : 'Centre',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '10 à 19 ans',
        'contact'          : '+33 1 84 60 12 34 | contact@safir-consulting.fr',
        'secteur_activite' : 'Conseil en Management et Systèmes d\'Information',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "Safir Consulting est un cabinet de conseil en management et "
            "systèmes d'information fondé en France en 2014, spécialisé dans "
            "les secteurs de la banque, de la finance et de l'assurance. Il "
            "accompagne les institutions financières africaines dans leur "
            "transformation digitale, la conformité aux réglementations "
            "prudentielles (Bâle III, IFRS), l'optimisation des processus "
            "métiers, la gouvernance IT et la gestion des risques opérationnels. "
            "Avec une connaissance approfondie de l'environnement réglementaire "
            "CEMAC et COBAC, Safir Consulting est un interlocuteur spécialisé "
            "pour les entreprises de services financiers camerounaises souhaitant "
            "renforcer leur conformité et moderniser leur architecture IT."
        ),
    },

    {
        'username'         : 'bc_pme',
        'raison_sociale'   : 'Banque Camerounaise des PME (BC-PME)',
        'region'           : 'Centre',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : '5 à 9 ans',
        'contact'          : '+237 222 70 00 00 | info@bcpme.cm',
        'secteur_activite' : 'Services Financiers et Bancaires',
        'statut'           : 'SARL',
        'classe'           : '2',
        'description'      : (
            "La Banque Camerounaise des Petites et Moyennes Entreprises "
            "(BC-PME) est l'institution publique spécifiquement dédiée au "
            "financement des PME camerounaises. Elle propose une gamme de "
            "produits financiers adaptés aux structures de taille "
            "intermédiaire : crédits d'investissement, crédits de campagne, "
            "lignes de crédit revolving, garanties bancaires et produits "
            "de trade finance. Son positionnement institutionnel et sa "
            "connaissance du tissu économique camerounais en font le "
            "partenaire financier naturel des entreprises établies "
            "cherchant à financer leur expansion ou leur modernisation "
            "dans un cadre adapté à leurs capacités de remboursement."
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
        'anciennete'       : '5 à 9 ans',
        'contact'          : '+237 690 12 34 56 | contact@fabrikaliments.com',
        'secteur_activite' : 'Conseil et Formation Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "Fabrik Aliments est le pionnier camerounais du conseil et de "
            "la formation en agroalimentaire en Afrique centrale. La structure "
            "propose aux petites entreprises agroalimentaires un annuaire de "
            "fournisseurs d'ingrédients et d'équipements, des services "
            "d'information sur les réglementations sanitaires et les normes "
            "de qualité, des formations techniques en transformation alimentaire "
            "et un accompagnement dans le développement de nouveaux produits "
            "à base d'ingrédients locaux. Partenaire de choix pour toute "
            "entreprise multi-sectorielle souhaitant développer une activité "
            "de transformation alimentaire conforme aux standards du marché."
        ),
    },

    {
        'username'         : 'nofia_cm',
        
        'raison_sociale'   : "Nouvelle Financière d'Afrique (NOFIA)",
        'region'           : 'Centre',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 à 9 ans',
        'contact'          : '+237 699 78 90 12 | nofia.microfinance@gmail.com',
        'secteur_activite' : 'Microfinance et Services Financiers',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "La Nouvelle Financière d'Afrique (NOFIA) est un établissement de "
            "microfinance camerounais sélectionné par le MINEPAT dans le cadre "
            "du programme de soutien au secteur privé en partenariat avec le "
            "PNUD (novembre 2024). Elle propose aux TPE et PME des lignes de "
            "crédit à taux bonifiés pour financer leurs besoins en fonds de "
            "roulement, en équipements et en développement commercial. "
            "Forte d'une connaissance fine des réalités économiques locales, "
            "NOFIA adapte ses produits financiers aux contraintes des petites "
            "entreprises multi-sectorielles en développement, avec des procédures "
            "simplifiées et des délais de traitement réduits."
        ),
    },

    {
        'username'         : 'focep_cm',
        'raison_sociale'   : "Fonds Camerounais d'Épargne pour le Progrès (FOCEP)",
        'region'           : 'Centre',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '10 à 19 ans',
        'contact'          : '+237 222 30 45 67 | focep@microfinance-cm.com',
        'secteur_activite' : 'Microfinance, Épargne et Crédit',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "Le Fonds Camerounais d'Épargne pour le Progrès (FOCEP) est un "
            "établissement de microfinance agréé par la COBAC, sélectionné "
            "par le MINEPAT et le PNUD pour le programme de soutien au secteur "
            "privé de 2024. Il propose aux entreprises en développement des "
            "produits d'épargne rémunérée, des crédits à court et moyen terme, "
            "des crédits de campagne et des services de transfert d'argent. "
            "Sa présence nationale et son ancrage communautaire lui permettent "
            "d'accompagner les petites entreprises multi-sectorielles de toutes "
            "les régions du Cameroun, y compris dans les zones rurales ou "
            "périurbaines moins couvertes par le réseau bancaire classique."
        ),
    },

    {
        'username'         : 'scr_cameroun',
        'raison_sociale'   : 'Société Camerounaise de Raffinage (SCR)',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+237 233 37 00 00 | contact@scr-cameroun.cm',
        'secteur_activite' : 'Transformation Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "La Société Camerounaise de Raffinage (SCR), implantée dans la "
            "Zone Industrielle de Bassa à Douala, est spécialisée dans la "
            "transformation des fruits du palmier à huile en huile végétale "
            "comestible raffinée, en savons et en margarines. Elle soutient "
            "les petits producteurs de palmier à huile en achetant leurs "
            "régimes à des prix garantis et en leur fournissant un encadrement "
            "technique. Avec une croissance de sa production de 15% en 2024 "
            "et des exportations vers l'Afrique de l'Ouest, la SCR constitue "
            "un débouché commercial stable et valorisant pour les petites "
            "entreprises agricoles du secteur oléagineux."
        ),
    },

    {
        'username'         : 'cameroon_tea',
        'raison_sociale'   : 'Cameroon Tea Estates (CTE)',
        'region'           : 'Ouest',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+237 233 45 10 00 | cte@cameroon-tea.cm',
        'secteur_activite' : 'Agriculture et Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "Cameroon Tea Estates (CTE), fondée en 1950, est le principal "
            "producteur de thé noir et vert du Cameroun, avec des plantations "
            "situées à Ndu, Tole et Djuttitsa dans la région de l'Ouest. "
            "Employant 4 000 personnes et produisant 10 000 tonnes de thé "
            "en 2023, CTE exporte vers l'Europe et l'Afrique tout en promouvant "
            "des pratiques agricoles biologiques certifiées. La société soutient "
            "les communautés locales via des infrastructures scolaires et "
            "sanitaires. Elle représente un modèle de durabilité et un partenaire "
            "commercial potentiel pour les petites entreprises souhaitant "
            "s'intégrer dans la filière thé camerounaise."
        ),
    },

    {
        'username'         : 'dhl_cameroun',
        'raison_sociale'   : 'DHL International Cameroon SARL',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+237 233 39 55 00 | cameroun.cs@dhl.com',
        'secteur_activite' : 'Transport, Logistique et Livraison Internationale',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "DHL International Cameroon SARL est la filiale camerounaise du "
            "groupe logistique mondial Deutsche Post DHL, leader mondial du "
            "transport express et de la logistique. Elle propose au Cameroun "
            "des services de livraison express nationale et internationale, "
            "de fret aérien et maritime, de gestion des douanes et de solutions "
            "e-commerce. Son réseau mondial couvrant plus de 220 pays et "
            "territoires permet aux petites entreprises camerounaises multi- "
            "sectorielles d'accéder à des marchés régionaux et internationaux "
            "avec des délais compétitifs et une traçabilité en temps réel de "
            "leurs envois."
        ),
    },

    {
        'username'         : 'africa_spices',
        'raison_sociale'   : 'Africa Spices Limited',
        'region'           : 'Littoral',
        'taille'           : 'Petite Entreprise',
        'anciennete'       : '5 à 9 ans',
        'contact'          : '+256 700 123 456 | info@africaspices.co.ug',
        'secteur_activite' : 'Transformation Agroalimentaire',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "Africa Spices Limited est une entreprise ougandaise spécialisée "
            "dans la fabrication, la commercialisation et la distribution "
            "d'épices et de mélanges d'assaisonnements à base d'herbes et "
            "légumes africains transformés en mélanges prêts à l'emploi. "
            "Distribuant ses produits dans l'ensemble de l'Afrique de l'Est "
            "et centrale, elle constitue un partenaire commercial potentiel "
            "pour les petites entreprises camerounaises du secteur agro- "
            "industriel souhaitant diversifier leur gamme de produits ou "
            "accéder aux marchés régionaux via des accords de distribution "
            "ou de co-développement produit."
        ),
    },

    {
        'username'         : 'massey_ferguson_cm',
        'raison_sociale'   : 'Massey Ferguson (AGCO Corporation)',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+27 11 928 6000 | africa@masseyferguson.com',
        'secteur_activite' : 'Fabrication de Machines et Équipements Agricoles',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "Massey Ferguson, marque phare d'AGCO Corporation, est l'un des "
            "fabricants de matériel agricole les plus implantés en Afrique "
            "subsaharienne. Sa gamme diversifiée de tracteurs, moissonneuses "
            "et équipements de post-récolte est reconnue pour sa robustesse "
            "et son rapport qualité-prix compétitif. La marque propose des "
            "solutions innovantes d'accès à l'équipement adaptées aux "
            "marchés africains, notamment des modèles de location basés sur "
            "les heures d'utilisation via des partenariats avec Hello Tractor. "
            "Ses distributeurs locaux au Cameroun assurent un service après- "
            "vente de proximité, essentiel pour les petites entreprises "
            "multi-sectorielles à ressources limitées."
        ),
    },

    {
        'username'         : 'new_holland_cm',
        'raison_sociale'   : 'CNH Industrial (New Holland Agriculture)',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+27 12 677 0000 | africa@newholland.com',
        'secteur_activite' : 'Fabrication de Machines Agricoles et Équipements',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "CNH Industrial, à travers ses marques New Holland Agriculture "
            "et Case IH, est l'un des principaux fabricants mondiaux de "
            "machines agricoles et équipements industriels. Sa gamme couvre "
            "les tracteurs compacts et de grande puissance, les équipements "
            "de récolte, de fenaison et de traitement des sols, adaptés aux "
            "différentes cultures et conditions climatiques africaines. "
            "Présent en Afrique centrale via un réseau de distributeurs "
            "agréés, CNH Industrial offre aux petites entreprises multi- "
            "sectorielles camerounaises un accès à des équipements agricoles "
            "fiables avec un support technique local et des solutions de "
            "financement adaptées."
        ),
    },

    {
        'username'         : 'mahindra_cm',
        'raison_sociale'   : 'Mahindra & Mahindra',
        'region'           : 'Littoral',
        'taille'           : 'Grande Entreprise',
        'anciennete'       : 'Plus de 20 ans',
        'contact'          : '+91 22 2490 1441 | africa@mahindra.com',
        'secteur_activite' : 'Fabrication de Machines Agricoles et Équipements',
        'statut'           : 'SARL',
        'classe'           : '3',
        'description'      : (
            "Mahindra & Mahindra est l'un des grands fabricants de tracteurs au "
            "monde en volume, fondé en Inde en 1945. Reconnu sur le marché "
            "africain pour la robustesse, la facilité de maintenance et le "
            "rapport qualité-prix très compétitif de ses équipements agricoles, "
            "Mahindra constitue une alternative économique aux grandes marques "
            "européennes et américaines, particulièrement adaptée aux marchés "
            "africains à revenus intermédiaires. Sa gamme de tracteurs compacts "
            "et ses équipements polyvalents répondent aux besoins diversifiés "
            "des petites entreprises multi-sectorielles camerounaises opérant "
            "dans plusieurs filières simultanément."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# 4. EXÉCUTION
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    import django
    
    # Configuration de l'environnement Django pour script autonome
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper.settings')
    django.setup()
    
    # Lancement de l'importation
    executer_importation()