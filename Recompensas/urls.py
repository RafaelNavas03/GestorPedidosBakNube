from django.urls import path
from .views import *

urlpatterns = [
    path('crear_recompensa_producto/', CrearRecompensaProducto.as_view(), name='crear_recompensa_producto'),
    path('crear_recompensa_combo/', CrearRecompensaCombo.as_view(), name='crear_recompensa_combo'),

]