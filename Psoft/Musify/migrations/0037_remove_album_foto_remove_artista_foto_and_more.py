# Generated by Django 5.0.2 on 2024-05-09 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0036_remove_usuario_generofavorito1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='foto',
        ),
        migrations.RemoveField(
            model_name='artista',
            name='foto',
        ),
        migrations.RemoveField(
            model_name='cancion',
            name='foto',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='foto',
        ),
        migrations.RemoveField(
            model_name='presentador',
            name='foto',
        ),
    ]
