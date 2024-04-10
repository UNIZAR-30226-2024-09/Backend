# Generated by Django 5.0.2 on 2024-04-10 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0006_delete_cantante'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancion',
            name='archivo_mp3',
            field=models.BinaryField(default=b'\x00'),
        ),
        migrations.AddField(
            model_name='cancion',
            name='foto',
            field=models.BinaryField(default=b'\x00'),
        ),
        migrations.AddField(
            model_name='capitulo',
            name='nombre',
            field=models.CharField(default='Nombre por defecto', max_length=255),
        ),
        migrations.DeleteModel(
            name='Favorito',
        ),
    ]
