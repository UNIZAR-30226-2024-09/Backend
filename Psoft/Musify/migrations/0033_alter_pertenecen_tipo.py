# Generated by Django 5.0.2 on 2024-05-01 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0032_alter_pertenecen_unique_together_pertenecen_tipo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pertenecen',
            name='tipo',
            field=models.CharField(max_length=255),
        ),
    ]