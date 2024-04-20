# Generated by Django 5.0.2 on 2024-04-20 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0011_remove_cancion_favorito'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usuario',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='password',
            field=models.CharField(default=None, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.CharField(max_length=255, primary_key=True, serialize=False, unique=True),
        ),
    ]
