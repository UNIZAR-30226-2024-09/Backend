# Generated by Django 5.0.2 on 2024-04-22 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0016_remove_puntuapodcast_mipodcast_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presentador',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('foto', models.BinaryField(default=b'\x00')),
                ('descripcion', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='cancion',
            old_name='archivo_mp3',
            new_name='archivoMp3',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='favorito',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='presentadores',
        ),
        migrations.AddField(
            model_name='album',
            name='foto',
            field=models.BinaryField(default=b'\x00'),
        ),
        migrations.AddField(
            model_name='artista',
            name='foto',
            field=models.BinaryField(default=b'\x00'),
        ),
        migrations.AddField(
            model_name='capitulo',
            name='archivoMp3',
            field=models.BinaryField(default=b'\x00'),
        ),
        migrations.AddField(
            model_name='podcast',
            name='foto',
            field=models.BinaryField(default=b'\x00'),
        ),
        migrations.CreateModel(
            name='Interpretan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('miPodcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musify.podcast')),
                ('miPresentador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musify.presentador')),
            ],
            options={
                'unique_together': {('miPresentador', 'miPodcast')},
            },
        ),
    ]