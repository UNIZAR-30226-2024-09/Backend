# Generated by Django 5.0.2 on 2024-05-10 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0037_remove_album_foto_remove_artista_foto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
