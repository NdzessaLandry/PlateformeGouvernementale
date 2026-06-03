from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
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

class CustomUser(AbstractUser):
    contact = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    raison_sociale = models.CharField(max_length=255, null=True, blank=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    statut = models.ForeignKey(Statut, on_delete=models.CASCADE, null=True, blank=True)
    secteur_activite = models.ForeignKey(SecteurActivite, on_delete=models.CASCADE, null=True, blank=True)
    taille = models.ForeignKey(Taille, on_delete=models.CASCADE, null=True, blank=True)
    anciennete = models.ForeignKey(Anciennete, on_delete=models.CASCADE, null=True, blank=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, null=True, blank=True)

