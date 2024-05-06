# Generated by Django 5.0.2 on 2024-05-02 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0034_pertenecencancion_pertenecenpodcast_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='artistaFavorito',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artistaFavorito', to='Musify.artista'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='generoFavorito1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='generoFavorito1', to='Musify.genero'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='generoFavorito2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='generoFavorito2', to='Musify.genero'),
        ),
    ]