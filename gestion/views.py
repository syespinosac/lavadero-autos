from django.shortcuts import render
from .models import Cliente, Vehiculo, Servicio, Factura
from django.utils import timezone
from django.db.models import Sum

def dashboard(request):
    hoy = timezone.now().date()

    # Calcular ingresos del día correctamente
    ingresos = Factura.objects.filter(
        fecha__date=hoy,
        estado='pagada'
    ).aggregate(total=Sum('total'))['total']

    # Si no hay facturas, mostrar 0
    if ingresos is None:
        ingresos = 0

    contexto = {
        'total_clientes':  Cliente.objects.count(),
        'total_vehiculos': Vehiculo.objects.count(),
        'servicios_hoy':   Servicio.objects.filter(fecha__date=hoy).count(),
        'ingresos_hoy':    ingresos,
    }
    return render(request, 'gestion/dashboard.html', contexto)