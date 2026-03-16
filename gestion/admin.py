from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (Usuario, Empleado, Cliente, 
                     Vehiculo, TipoServicio, 
                     Servicio, Factura, DetalleFactura)

admin.site.register(Usuario)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(TipoServicio)
admin.site.register(Servicio)
admin.site.register(Factura)
admin.site.register(DetalleFactura)