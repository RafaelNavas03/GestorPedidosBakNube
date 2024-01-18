from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Proveedores
from Administrador.models import Administrador

@method_decorator(csrf_exempt, name='dispatch')
class CrearProveedor(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            nombre_proveedor = request.POST.get('nombre_proveedor')
            direccion_proveedor = request.POST.get('direccion_proveedor')
            telefono_proveedor = request.POST.get('telefono_proveedor')
            correo_proveedor = request.POST.get('correo_proveedor')
            estado_proveedor = request.POST.get('estado_proveedor')

            if not nombre_proveedor or not estado_proveedor:
                raise ValueError("Nombre proveedor y estado son obligatorios")

            id_administrador = Administrador.objects.first()

            proveedor = Proveedores(
                nombreproveedor=nombre_proveedor,
                direccionproveedor=direccion_proveedor,
                telefonoproveedor=telefono_proveedor,
                correoproveedor=correo_proveedor,
                id_administrador=id_administrador,
                sestado=estado_proveedor
            )

            proveedor.save()

            return JsonResponse({'mensaje': 'Proveedor creado con éxito'})
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class EditarProveedor(View):
    @transaction.atomic
    def post(self, request, proveedor_id, *args, **kwargs):
        try:
            proveedor = Proveedores.objects.get(id_proveedor=proveedor_id)

            nombre_proveedor = request.POST.get('nombre_proveedor')
            direccion_proveedor = request.POST.get('direccion_proveedor')
            telefono_proveedor = request.POST.get('telefono_proveedor')
            correo_proveedor = request.POST.get('correo_proveedor')
            estado_proveedor = request.POST.get('estado_proveedor')

            proveedor.nombreproveedor = nombre_proveedor
            proveedor.direccionproveedor = direccion_proveedor
            proveedor.telefonoproveedor = telefono_proveedor
            proveedor.correoproveedor = correo_proveedor
            proveedor.sestado = estado_proveedor

            proveedor.save()

            return JsonResponse({'mensaje': 'Proveedor editado con éxito'})
        except Proveedores.DoesNotExist:
            return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)