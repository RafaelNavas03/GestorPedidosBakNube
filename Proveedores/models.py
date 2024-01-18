from django.db import models
from Administrador.models import Administrador

class Proveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True, db_column='id_proveedor')
    nombreproveedor = models.CharField(max_length=300, db_column='nombreproveedor')
    direccionproveedor = models.CharField(max_length=300, blank=True, null=True, db_column='direccionproveedor')
    telefonoproveedor = models.CharField(max_length=10, blank=True, null=True, db_column='telefonoproveedor')
    correoproveedor = models.CharField(max_length=256, blank=True, null=True, db_column='correoproveedor')
    id_administrador = models.ForeignKey(Administrador, on_delete=models.DO_NOTHING, db_column='id_administrador')
    sestado = models.CharField(max_length=1, choices=[('0', '0'), ('1', '1')], db_column='sestado')

    class Meta:
        managed = False
        db_table = 'proveedores'
