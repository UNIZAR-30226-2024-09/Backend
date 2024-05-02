# Generated by Django 5.0.2 on 2024-05-02 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0033_alter_pertenecen_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PertenecenCancion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miCancion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musify.cancion')),
                ('miGenero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musify.genero')),
            ],
            options={
                'unique_together': {('miGenero', 'miCancion')},
            },
        ),
        migrations.CreateModel(
            name='PertenecenPodcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miGenero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musify.genero')),
                ('miPodcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musify.podcast')),
            ],
            options={
                'unique_together': {('miGenero', 'miPodcast')},
            },
        ),
        migrations.DeleteModel(
            name='Pertenecen',
        ),
    ]