# Generated by Django 5.0.2 on 2024-03-10 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0004_cantante_remove_cancion_letra_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artista',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cancion',
            name='cantantes',
        ),
        migrations.AddField(
            model_name='cancion',
            name='cantantes',
            field=models.ManyToManyField(to='Musify.artista'),
        ),
    ]