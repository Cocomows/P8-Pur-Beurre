from django.db import models

# Create your models here.


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
    brand = models.CharField(verbose_name="Marque", max_length=100)
    nutriscore = models.SmallIntegerField(choices=NUTRISCORE_CHOICES, default=0)
    description = models.TextField()
    image = models.URLField()
    link_openfoodfacts = models.URLField(verbose_name="URL Openfoodfacts", )

    def __str__(self):
        return self.name

