# Generated by Django 5.0.2 on 2024-04-23 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0020_rename_seguidos_seguido_rename_seguidores_seguidor'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Amigo',
        ),
    ]