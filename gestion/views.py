from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  
from .models import Cliente, Vehiculo, Servicio, Factura
from .models import Cliente, Vehiculo, Servicio, Factura, Empleado
from .models import Cliente, Vehiculo, Servicio, Factura, Empleado, TipoServicio
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



# ─────────────────────────────────────────
# EMPLEADOS
# ─────────────────────────────────────────
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleados.html', {'empleados': empleados})


def nuevo_empleado(request):
    if request.method == 'POST':
        nombre    = request.POST['nombre']
        telefono  = request.POST['telefono']
        porcentaje_comision = request.POST['porcentaje_comision']
        Empleado.objects.create(
            nombre=nombre,
            telefono=telefono,
            porcentaje_comision=porcentaje_comision
        )
        messages.success(request, '✅ Empleado creado exitosamente')
        return redirect('lista_empleados')
    return render(request, 'gestion/nuevo_empleado.html')


def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.nombre              = request.POST['nombre']
        empleado.telefono            = request.POST['telefono']
        empleado.porcentaje_comision = request.POST['porcentaje_comision']
        empleado.save()
        messages.success(request, '✅ Empleado actualizado exitosamente')
        return redirect('lista_empleados')
    return render(request, 'gestion/editar_empleado.html', {'empleado': empleado})


def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    empleado.delete()
    messages.success(request, '🗑️ Empleado eliminado exitosamente')
    return redirect('lista_empleados')

# ─────────────────────────────────────────
# TIPOS DE SERVICIO
# ─────────────────────────────────────────
def lista_tipos_servicio(request):
    tipos = TipoServicio.objects.all()
    return render(request, 'gestion/tipos_servicio.html', {'tipos': tipos})


def nuevo_tipo_servicio(request):
    if request.method == 'POST':
        TipoServicio.objects.create(
            nombre      = request.POST['nombre'],
            descripcion = request.POST['descripcion'],
            precio      = request.POST['precio'],
        )
        messages.success(request, '✅ Tipo de servicio creado exitosamente')
        return redirect('lista_tipos_servicio')
    return render(request, 'gestion/nuevo_tipo_servicio.html')


def editar_tipo_servicio(request, id):
    tipo = get_object_or_404(TipoServicio, id=id)
    if request.method == 'POST':
        tipo.nombre      = request.POST['nombre']
        tipo.descripcion = request.POST['descripcion']
        tipo.precio      = request.POST['precio']
        tipo.activo      = 'activo' in request.POST
        tipo.save()
        messages.success(request, '✅ Tipo de servicio actualizado exitosamente')
        return redirect('lista_tipos_servicio')
    return render(request, 'gestion/editar_tipo_servicio.html', {'tipo': tipo})


def eliminar_tipo_servicio(request, id):
    tipo = get_object_or_404(TipoServicio, id=id)
    tipo.delete()
    messages.success(request, '🗑️ Tipo de servicio eliminado exitosamente')
    return redirect('lista_tipos_servicio')


# ─────────────────────────────────────────
# SERVICIOS
# ─────────────────────────────────────────
def lista_servicios(request):
    servicios = Servicio.objects.all().order_by('-fecha')
    return render(request, 'gestion/servicios.html', {'servicios': servicios})


def nuevo_servicio(request):
    vehiculos = Vehiculo.objects.all()
    empleados = Empleado.objects.all()
    tipos     = TipoServicio.objects.filter(activo=True)

    if request.method == 'POST':
        vehiculo_id      = request.POST['vehiculo']
        empleado_id      = request.POST['empleado']
        tipo_servicio_id = request.POST['tipo_servicio']
        observaciones    = request.POST['observaciones']

        # Obtener el precio del tipo de servicio
        tipo = TipoServicio.objects.get(id=tipo_servicio_id)
        empleado = Empleado.objects.get(id=empleado_id)

        # Calcular comisión automáticamente
        comision = tipo.precio * (empleado.porcentaje_comision / 100)

        Servicio.objects.create(
            vehiculo_id      = vehiculo_id,
            empleado_id      = empleado_id,
            tipo_servicio_id = tipo_servicio_id,
            precio           = tipo.precio,
            comision         = comision,
            observaciones    = observaciones,
        )
        messages.success(request, '✅ Servicio registrado exitosamente')
        return redirect('lista_servicios')

    return render(request, 'gestion/nuevo_servicio.html', {
        'vehiculos': vehiculos,
        'empleados': empleados,
        'tipos':     tipos,
    })


def editar_servicio(request, id):
    servicio  = get_object_or_404(Servicio, id=id)
    vehiculos = Vehiculo.objects.all()
    empleados = Empleado.objects.all()
    tipos     = TipoServicio.objects.filter(activo=True)

    if request.method == 'POST':
        tipo     = TipoServicio.objects.get(id=request.POST['tipo_servicio'])
        empleado = Empleado.objects.get(id=request.POST['empleado'])

        servicio.vehiculo_id      = request.POST['vehiculo']
        servicio.empleado_id      = request.POST['empleado']
        servicio.tipo_servicio_id = request.POST['tipo_servicio']
        servicio.estado           = request.POST['estado']
        servicio.precio           = tipo.precio
        servicio.comision         = tipo.precio * (empleado.porcentaje_comision / 100)
        servicio.observaciones    = request.POST['observaciones']
        servicio.save()

        messages.success(request, '✅ Servicio actualizado exitosamente')
        return redirect('lista_servicios')

    return render(request, 'gestion/editar_servicio.html', {
        'servicio':  servicio,
        'vehiculos': vehiculos,
        'empleados': empleados,
        'tipos':     tipos,
    })


def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    messages.success(request, '🗑️ Servicio eliminado exitosamente')
    return redirect('lista_servicios')