from django.views import View
from django.http import JsonResponse
from django.db import transaction
from .models import RecompensasCombos, RecompensasProductos
from Combos.models import Combo
from Producto.models import Producto
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class CrearRecompensaCombo(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_combo = request.POST.get('id_combo')
            puntos_recompensa_combo = request.POST.get('puntos_recompensa_combo')
            sestado = request.POST.get('sestado')

            combo = Combo.objects.get(id_combo=id_combo)
            recompensa_combo = RecompensasCombos.objects.create(
                id_combo=combo,
                puntos_recompensa_combo=puntos_recompensa_combo,
                sestado=sestado
            )
            recompensa_combo.save()

            return JsonResponse({'mensaje': 'Recompensa de combo creada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class CrearRecompensaProducto(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_producto = request.POST.get('id_producto')
            puntos_recompensa_producto = request.POST.get('puntos_recompensa_producto')
            sestado = request.POST.get('sestado')

            producto = Producto.objects.get(id_producto=id_producto)
            recompensa_producto = RecompensasProductos.objects.create(
                id_producto=producto,
                puntos_recompensa_producto=puntos_recompensa_producto,
                sestado=sestado
            )
            recompensa_producto.save()

            return JsonResponse({'mensaje': 'Recompensa de producto creada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)