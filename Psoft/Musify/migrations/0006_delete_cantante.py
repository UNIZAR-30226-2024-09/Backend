# Generated by Django 5.0.2 on 2024-03-13 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0005_artista_remove_cancion_cantantes_delete_cantante_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cantante',
        ),
    ]
