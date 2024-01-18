# Generated by Django 5.0 on 2024-01-12 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horariossemanales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleHorariosSemanales',
            fields=[
                ('id_dethorarios', models.AutoField(primary_key=True, serialize=False)),
                ('dia', models.CharField(choices=[('L', 'Lunes'), ('M', 'Martes'), ('X', 'Miércoles'), ('J', 'Jueves'), ('V', 'Viernes'), ('S', 'Sábado'), ('D', 'Domingo')], max_length=1)),
                ('horainicio', models.TimeField()),
                ('horafin', models.TimeField()),
            ],
            options={
                'db_table': 'detallehorariossemanales',
                'managed': False,
            },
        ),
    ]