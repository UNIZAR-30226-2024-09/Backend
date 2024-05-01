# Generated by Django 5.0.2 on 2024-05-01 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0031_rename_miusuario_seguido_miusuarioseguido_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pertenecen',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='pertenecen',
            name='tipo',
            field=models.CharField(default='Cancion', max_length=255),
        ),
        migrations.AlterField(
            model_name='pertenecen',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterUniqueTogether(
            name='pertenecen',
            unique_together={('miGenero', 'miAudio', 'tipo')},
        ),
    ]
