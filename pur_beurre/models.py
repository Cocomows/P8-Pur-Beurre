from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    NUTRISCORE_CHOICES = (
        (0, "N/A"),
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D"),
        (5, "E"),

    )
    name = models.CharField(verbose_name="Nom", max_length=100)
    code = models.CharField(verbose_name="Code", max_length=20, primary_key=True, default="0")
    brand = models.CharField(verbose_name="Marque", max_length=100, blank=True)
    nutriscore = models.SmallIntegerField(choices=NUTRISCORE_CHOICES, default=0, blank=True)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    link_openfoodfacts = models.URLField(verbose_name="URL Openfoodfacts", blank=True )
    saved_by = models.ManyToManyField(User, verbose_name="Sauvegardé par", blank=True)

    def __str__(self):
        return self.name

