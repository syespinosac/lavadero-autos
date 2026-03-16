from django.db import models

# Create your models here.
# ─────────────────────────────────────────
# TABLA USUARIOS Y ROLES
# ─────────────────────────────────────────
class Usuario(models.Model):
    ROLES = [
        ('admin',    'Administrador'),
        ('empleado', 'Empleado'),
    ]
    nombre     = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol        = models.CharField(max_length=20, choices=ROLES, default='empleado')
    activo     = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.rol})"


# ─────────────────────────────────────────
# TABLA EMPLEADOS
# ─────────────────────────────────────────
class Empleado(models.Model):
    usuario       = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre        = models.CharField(max_length=100)
    telefono      = models.CharField(max_length=20)
    fecha_ingreso = models.DateField(auto_now_add=True)
    porcentaje_comision = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)

    def __str__(self):
        return self.nombre


# ─────────────────────────────────────────
# TABLA CLIENTES
# ─────────────────────────────────────────
class Cliente(models.Model):
    nombre          = models.CharField(max_length=100)
    telefono        = models.CharField(max_length=20)
    email           = models.EmailField(blank=True, null=True)
    fecha_registro  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


# ─────────────────────────────────────────
# TABLA VEHICULOS
# ─────────────────────────────────────────
class Vehiculo(models.Model):
    TIPOS = [
        ('sedan',  'Sedán'),
        ('suv',    'SUV'),
        ('moto',   'Moto'),
        ('camion', 'Camión'),
        ('otro',   'Otro'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    placa   = models.CharField(max_length=10, unique=True)
    marca   = models.CharField(max_length=50)
    color   = models.CharField(max_length=30)
    tipo    = models.CharField(max_length=20, choices=TIPOS, default='sedan')

    def __str__(self):
        return f"{self.placa} - {self.marca} ({self.cliente.nombre})"


# ─────────────────────────────────────────
# TABLA TIPOS DE SERVICIO
# ─────────────────────────────────────────
class TipoServicio(models.Model):
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    activo      = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


# ─────────────────────────────────────────
# TABLA SERVICIOS (la más importante)
# ─────────────────────────────────────────
class Servicio(models.Model):
    ESTADOS = [
        ('pendiente',   'Pendiente'),
        ('en_proceso',  'En Proceso'),
        ('listo',       'Listo'),
        ('entregado',   'Entregado'),
    ]
    vehiculo      = models.ForeignKey(Vehiculo,     on_delete=models.CASCADE)
    empleado      = models.ForeignKey(Empleado,     on_delete=models.CASCADE)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    fecha         = models.DateTimeField(auto_now_add=True)
    precio        = models.DecimalField(max_digits=10, decimal_places=2)
    estado        = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    comision      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True, null=True)

    def calcular_comision(self):
        self.comision = self.precio * (self.empleado.porcentaje_comision / 100)
        return self.comision

    def __str__(self):
        return f"{self.vehiculo.placa} - {self.tipo_servicio.nombre} - {self.estado}"
    

    # FACTURA
class Factura(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada',    'Pagada'),
        ('anulada',   'Anulada'),
    ]
    METODOS_PAGO = [
        ('efectivo',      'Efectivo'),
        ('tarjeta',       'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]
    numero        = models.AutoField(primary_key=True)
    cliente       = models.ForeignKey(Cliente,  on_delete=models.CASCADE)
    empleado      = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha         = models.DateTimeField(auto_now_add=True)
    subtotal      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total         = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado        = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    metodo_pago   = models.CharField(max_length=20, choices=METODOS_PAGO, default='efectivo')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Factura #{self.numero} - {self.cliente.nombre} - ${self.total}"


# DETALLE FACTURA
class DetalleFactura(models.Model):
    factura          = models.ForeignKey(Factura,      on_delete=models.CASCADE)
    tipo_servicio    = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    empleado         = models.ForeignKey(Empleado,     on_delete=models.CASCADE)
    vehiculo         = models.ForeignKey(Vehiculo,     on_delete=models.CASCADE)
    cantidad         = models.IntegerField(default=1)
    precio_unitario  = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal         = models.DecimalField(max_digits=10, decimal_places=2)
    comision         = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.tipo_servicio.nombre} x{self.cantidad} - ${self.subtotal}"