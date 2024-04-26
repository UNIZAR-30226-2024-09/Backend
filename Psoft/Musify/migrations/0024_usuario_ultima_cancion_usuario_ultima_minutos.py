# Generated by Django 5.0.2 on 2024-04-26 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0023_remove_usuario_artistas_favoritos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='ultima_cancion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ultima_cancion', to='Musify.cancion'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='ultima_minutos',
            field=models.IntegerField(default=0),
        ),
    ]
