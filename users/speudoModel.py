from django.db import models

class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    libele = models.CharField(max_length=255)

    def __str__(self):
        return self.libele


class Statut(models.Model):
    id_statut = models.AutoField(primary_key=True)
    libele = models.CharField(max_length=255)

    def __str__(self):
        return self.libele


class SecteurActivite(models.Model):
    id_secteur_activite = models.AutoField(primary_key=True)
    libele = models.CharField(max_length=255)

    def __str__(self):
        return self.libele


class Taille(models.Model):
    id_taille = models.AutoField(primary_key=True)
    libele = models.CharField(max_length=255)

    def __str__(self):
        return self.libele


class Anciennete(models.Model):
    id_anciennete = models.AutoField(primary_key=True)
    libele = models.CharField(max_length=255)

    def __str__(self):
        return self.libele


class Classe(models.Model):
    id_classe = models.AutoField(primary_key=True)
    libele = models.CharField(max_length=255)

    def __str__(self):
        return self.libele


class Entreprise(models.Model):
    id_entreprise = models.AutoField(primary_key=True)
    contact = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    raison_sociale = models.CharField(max_length=255)

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    statut = models.ForeignKey(Statut, on_delete=models.CASCADE)
    secteur_activite = models.ForeignKey(SecteurActivite, on_delete=models.CASCADE)
    taille = models.ForeignKey(Taille, on_delete=models.CASCADE)
    anciennete = models.ForeignKey(Anciennete, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)

    def __str__(self):
        return self.raison_sociale


class ReponseBesoins(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('entreprise', 'classe')
