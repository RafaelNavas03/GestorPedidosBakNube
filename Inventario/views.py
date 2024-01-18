from django.shortcuts import render
from Inventario.models import Inventario
from Producto.models import *
from Bodega.models import Bodegas
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class CrearInventario(View):
    def post(self, request, *args, **kwargs):
        try:
            id_componente = request.POST.get('id_componente')
            id_producto = request.POST.get('id_producto')

            if id_componente and id_producto:
                raise ValueError('Debe ingresar solo un componente o un producto, no ambos.')

            costo_unitario = request.POST.get('costo_unitario')
            id_um = request.POST.get('id_um')
            stock_minimo = request.POST.get('stock_minimo')
            cantidad_disponible = request.POST.get('cantidad_disponible')

            id_bodega = request.POST.get('id_bodega')
            bodega_instance = Bodegas.objects.get(id_bodega=id_bodega)

            if id_producto:
                producto_instance = Producto.objects.get(id_producto=id_producto)
                componente_instance = None
            elif id_componente:
                componente_instance = Componente.objects.get(id_componente=id_componente)
                producto_instance = None
            else:
                raise ValueError('Debe ingresar un componente o un producto.')

            id_um = request.POST.get('id_um')
            um_instance = UnidadMedida.objects.get(idum=id_um)

            inventario = Inventario.objects.create(
                id_bodega=bodega_instance,
                id_producto=producto_instance,
                id_componente=componente_instance,
                costo_unitario=costo_unitario,
                id_um=um_instance,
                stock_minimo=stock_minimo,
                cantidad_disponible=cantidad_disponible
            )
            inventario.save()

            return JsonResponse({'mensaje': 'Inventario creado con éxito'})
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
                    'id_um': inventario.id_um.idum,
                    'stock_minimo': str(inventario.stock_minimo),
                    'cantidad_disponible': str(inventario.cantidad_disponible),
                })

            return JsonResponse({'inventario': inventario_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)