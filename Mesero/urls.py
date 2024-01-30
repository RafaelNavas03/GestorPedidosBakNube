from django.urls import path
from .views import *

urlpatterns = [
    path('tomar_pedido/<int:id_mesero>/', TomarPedido.as_view(), name='tomar_pedido'),
]
