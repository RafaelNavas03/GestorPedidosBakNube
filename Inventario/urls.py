from django.urls import path
from .views import * 

urlpatterns = [
    path('crearinventario/', CrearInventario.as_view(), name='crearinventario'),
    path('verinventario/', ListarInventario.as_view(), name='verinventario'),
    path('editar/<int:id_inventario>/', EditarInventario.as_view(), name='editar_inventario'),
]
