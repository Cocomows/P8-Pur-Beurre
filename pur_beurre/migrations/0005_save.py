# Generated by Django 2.1 on 2018-09-20 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pur_beurre', '0004_auto_20180917_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Save',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True, verbose_name='Date sauvegarde')),
            ],
        ),
    ]
