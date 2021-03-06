# Generated by Django 2.1 on 2018-09-20 13:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pur_beurre', '0005_save'),
    ]

    operations = [
        migrations.AddField(
            model_name='save',
            name='saved_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Sauvegardé par'),
        ),
        migrations.AddField(
            model_name='save',
            name='saved_product',
            field=models.ManyToManyField(to='pur_beurre.Product', verbose_name='Produit sauvegardé'),
        ),
    ]
