# Generated by Django 5.0.2 on 2024-04-25 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0022_usuario_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='artistas_favoritos',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='generos_favoritos',
        ),
    ]
