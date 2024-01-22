from django.shortcuts import render
from Inventario.models import Inventario
from Producto.models import *
from Bodega.models import Bodegas
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from decimal import Decimal 
from Proveedores.models import *
import json

@method_decorator(csrf_exempt, name='dispatch')
class CrearInventario(View):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener datos del pedido desde el request
            data = json.loads(request.body.decode('utf-8'))

            id_proveedor = data.get('id_proveedor')
            id_bodega = data.get('id_bodega')
            fecha_pedido = data.get('fecha_pedido')
            fecha_entrega_esperada = data.get('fecha_entrega_esperada')
            observacion_pedido = data.get('observacion_pedido')

            proveedor_instance = get_object_or_404(Proveedores, id_proveedor=id_proveedor)
            bodega_instance = get_object_or_404(Bodegas, id_bodega=id_bodega)

            # Crear el pedido
            pedido = Pedidosproveedor.objects.create(
                id_proveedor=proveedor_instance,
                id_bodega=bodega_instance,
                fechapedido=fecha_pedido,
                fechaentregaesperada=fecha_entrega_esperada,
                estado='P',
                observacion=observacion_pedido
            )
            
            detalles_pedido_raw = data.get('detalles_pedido')
            detalles_pedido = json.loads(detalles_pedido_raw)

            # Iterar sobre los detalles del pedido
            for detalle_pedido_data in detalles_pedido:
                # Obtener datos del detalle del pedido desde el request
                id_producto = detalle_pedido_data.get('id_producto')
                id_componente = detalle_pedido_data.get('id_componente')
                cantidad_pedido = detalle_pedido_data.get('cantidad_pedido')
                costo_unitario = detalle_pedido_data.get('costo_unitario')
                id_um = detalle_pedido_data.get('id_um')
                stock_minimo = detalle_pedido_data.get('stock_minimo')

                if id_producto:
                    producto_instance = get_object_or_404(Producto, id_producto=id_producto)
                    componente_instance = None
                elif id_componente:
                    componente_instance = get_object_or_404(Componente, id_componente=id_componente)
                    producto_instance = None
                else:
                    raise ValueError('Debe ingresar un componente o un producto.')

                if componente_instance and id_um:
                    raise ValueError('El componente no requiere una unidad de medida.')

                if id_um:
                    um_instance = get_object_or_404(UnidadMedida, idum=id_um)
                else:
                    um_instance = None

                # Crear el detalle del pedido
                detalle_pedido = Detallepedidoproveedor.objects.create(
                    id_pedidoproveedor=pedido,
                    id_producto=producto_instance,
                    id_componente=componente_instance,
                    cantidad=cantidad_pedido,
                    costounitario=costo_unitario,
                    id_um=um_instance
                )

                # Actualizar el inventario
                inventario, created = Inventario.objects.get_or_create(
                    id_bodega=bodega_instance,
                    id_producto=producto_instance,
                    id_componente=componente_instance,
                    id_um=um_instance,
                    defaults={'stock_minimo': stock_minimo, 'cantidad_disponible': cantidad_pedido}
                )

                if not created:
                    # Si ya existe el registro en el inventario, actualiza la cantidad disponible
                    inventario.cantidad_disponible += cantidad_pedido
                    inventario.save()

            return JsonResponse({'mensaje': 'Pedido y inventario creados con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ListarInventario(View):
    def get(self, request, *args, **kwargs):
        try:
            inventario_list = Inventario.objects.all()
            inventario_data = []

            for inventario in inventario_list:
                inventario_data.append({
                    'id_inventario': inventario.id_inventario,
                    'id_bodega': inventario.id_bodega.id_bodega,
                    'id_producto': inventario.id_producto.id_producto if inventario.id_producto else None,
                    'id_componente': inventario.id_componente.id_componente if inventario.id_componente else None,
                    'costo_unitario': str(inventario.costo_unitario),
                    'id_um': inventario.id_um.idum if inventario.id_um else None,
                    'stock_minimo': str(inventario.stock_minimo),
                    'cantidad_disponible': str(inventario.cantidad_disponible),
                })

            return JsonResponse({'inventario': inventario_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class EditarInventario(View):
    def post(self, request, *args, **kwargs):
        try:
            id_inventario = kwargs.get('id_inventario')
            cantidad_aumentar = request.POST.get('cantidad_aumentar') 
            nuevo_stock_minimo = request.POST.get('nuevo_stock_minimo')
            nuevo_costo_unitario = request.POST.get('nuevo_costo_unitario')

            inventario = get_object_or_404(Inventario, id_inventario=id_inventario)

            if cantidad_aumentar:
                cantidad_aumentar = Decimal(cantidad_aumentar)
                inventario.cantidad_disponible += cantidad_aumentar

            if nuevo_stock_minimo:
                nuevo_stock_minimo = Decimal(nuevo_stock_minimo)
                inventario.stock_minimo = nuevo_stock_minimo

            if nuevo_costo_unitario:
                nuevo_costo_unitario = Decimal(nuevo_costo_unitario)
                inventario.costo_unitario = nuevo_costo_unitario

            inventario.save()

            return JsonResponse({'mensaje': 'Inventario actualizado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
