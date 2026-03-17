from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  
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
        messages.success(request, '✅ Cliente creado exitosamente')
        return redirect('lista_clientes')
    return render(request, 'gestion/nuevo_cliente.html')


def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.nombre   = request.POST['nombre']
        cliente.telefono = request.POST['telefono']
        cliente.email    = request.POST['email']
        cliente.save()
        messages.success(request, '✅ Cliente actualizado exitosamente')
        return redirect('lista_clientes')
    return render(request, 'gestion/editar_cliente.html', {'cliente': cliente})


def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, '🗑️ Cliente eliminado exitosamente')
    return redirect('lista_clientes')


# ─────────────────────────────────────────
# VEHICULOS
# ─────────────────────────────────────────
def lista_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'gestion/vehiculos.html', {'vehiculos': vehiculos})


def nuevo_vehiculo(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        Vehiculo.objects.create(
            cliente_id = request.POST['cliente'],
            placa      = request.POST['placa'],
            marca      = request.POST['marca'],
            color      = request.POST['color'],
            tipo       = request.POST['tipo']
        )
        messages.success(request, '✅ Vehículo registrado exitosamente')
        return redirect('lista_vehiculos')
    return render(request, 'gestion/nuevo_vehiculo.html', {'clientes': clientes})


def editar_vehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        vehiculo.cliente_id = request.POST['cliente']
        vehiculo.placa      = request.POST['placa']
        vehiculo.marca      = request.POST['marca']
        vehiculo.color      = request.POST['color']
        vehiculo.tipo       = request.POST['tipo']
        vehiculo.save()
        messages.success(request, '✅ Vehículo actualizado exitosamente')
        return redirect('lista_vehiculos')
    return render(request, 'gestion/editar_vehiculo.html', {
        'vehiculo': vehiculo,
        'clientes': clientes
    })


def eliminar_vehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()
    messages.success(request, '🗑️ Vehículo eliminado exitosamente')
    return redirect('lista_vehiculos')