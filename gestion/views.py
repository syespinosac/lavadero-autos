from django.shortcuts import render, redirect, get_object_or_404
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

# ─────────────────────────────────────────
# CLIENTES
# ─────────────────────────────────────────
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {'clientes': clientes})


def nuevo_cliente(request):
    if request.method == 'POST':
        nombre   = request.POST['nombre']
        telefono = request.POST['telefono']
        email    = request.POST['email']
        Cliente.objects.create(
            nombre=nombre,
            telefono=telefono,
            email=email
        )
        return redirect('lista_clientes')
    return render(request, 'gestion/nuevo_cliente.html')


def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.nombre   = request.POST['nombre']
        cliente.telefono = request.POST['telefono']
        cliente.email    = request.POST['email']
        cliente.save()
        return redirect('lista_clientes')
    return render(request, 'gestion/editar_cliente.html', {'cliente': cliente})


def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('lista_clientes')