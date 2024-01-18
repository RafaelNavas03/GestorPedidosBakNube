from django.urls import path
from .views import *

urlpatterns = [
    path('crear/', CrearMesa.as_view(), name='crearmesa'),
    path('ver_mesas/', MostrarMesas.as_view(), name='MostrarMesas'),
    path('editar_mesa/<int:id_mesa>/', EditarMesa.as_view(), name='editar_mesa'),
]