# Generated by Django 5.0.2 on 2024-03-05 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Musify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cola',
            name='miAudio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musify.cancion'),
        ),
        migrations.AlterField(
            model_name='favorito',
            name='miAudio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='veces_marcado_favorito', to='Musify.cancion'),
        ),
        migrations.AlterField(
            model_name='historial',
            name='miAudio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='veces_escuchado', to='Musify.cancion'),
        ),
        migrations.AlterField(
            model_name='pertenecen',
            name='miAudio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musify.cancion'),
        ),
        migrations.AlterField(
            model_name='contiene',
            name='miAudio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists_que_lo_contienen', to='Musify.cancion'),
        ),
        migrations.AddField(
            model_name='cancion',
            name='nombre',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cancion',
            name='puntuacion',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Audio',
        ),
    ]
