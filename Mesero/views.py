import json
import traceback
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import datetime
from Mesero.models import *

@method_decorator(csrf_exempt, name='dispatch')
class TomarPedido(View):
    def post(self, request, id_mesero, *args, **kwargs):
        try:
            # Obtener datos del pedido desde el request
            mesero_instance = get_object_or_404(Meseros, id_mesero=id_mesero)
            id_mesa = request.POST.get('id_mesa')
            id_cliente = request.POST.get('id_cliente')
            fecha_pedido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tipo_de_pedido = request.POST.get('tipo_de_pedido')
            metodo_de_pago = request.POST.get('metodo_de_pago')
            puntos = request.POST.get('puntos')
            fecha_entrega = request.POST.get('fecha_entrega')  # Puedes ajustar este campo según tus necesidades
            estado_del_pedido = request.POST.get('estado_del_pedido')
            observacion_del_cliente = request.POST.get('observacion_del_cliente')

            # Crear el pedido
            nuevo_pedido = Pedidos.objects.create(
                id_cliente=id_cliente,
                precio=0,  # Puedes ajustar este campo según tus necesidades
                tipo_de_pedido=tipo_de_pedido,
                metodo_de_pago=metodo_de_pago,
                puntos=puntos,
                fecha_pedido=fecha_pedido,
                fecha_entrega=fecha_entrega,
                estado_del_pedido=estado_del_pedido,
                observacion_del_cliente=observacion_del_cliente,
            )

            # Asociar el pedido con el mesero y la mesa
            mesero_instance = get_object_or_404(Meseros, id_mesero=id_mesero)
            mesa_instance = get_object_or_404(Mesas, id_mesa=id_mesa)
            Pedidosmesa.objects.create(
                id_mesero=mesero_instance,
                id_mesa=mesa_instance,
                id_pedido=nuevo_pedido,
            )

            detalles_pedido_raw = request.POST.get('detalles_pedido', '{}')
            detalles_pedido = json.loads(detalles_pedido_raw)

            # Iterar sobre los detalles del pedido
            for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                id_producto = detalle_pedido_data.get('id_producto')
                id_combo = detalle_pedido_data.get('id_combo')
                id_promocion = detalle_pedido_data.get('id_promocion')
                cantidad = detalle_pedido_data['cantidad']
                precio_unitario = detalle_pedido_data['precio_unitario']
                impuesto = detalle_pedido_data['impuesto']
                descuento = detalle_pedido_data['descuento']

                Detallepedidos.objects.create(
                    id_pedido=nuevo_pedido,
                    id_producto=id_producto,
                    id_combo=id_combo,
                    id_promocion=id_promocion,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    impuesto=impuesto,
                    descuento=descuento,
                )
            return JsonResponse({'mensaje': 'Pedido creado con éxito'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)
