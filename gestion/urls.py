from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

     # Clientes
    path('clientes/',                     views.lista_clientes,   name='lista_clientes'),
    path('clientes/nuevo/',               views.nuevo_cliente,    name='nuevo_cliente'),
    path('clientes/editar/<int:id>/',     views.editar_cliente,   name='editar_cliente'),
    path('clientes/eliminar/<int:id>/',   views.eliminar_cliente, name='eliminar_cliente'),

    # Vehiculos
    path('vehiculos/',                      views.lista_vehiculos,  name='lista_vehiculos'),
    path('vehiculos/nuevo/',                views.nuevo_vehiculo,   name='nuevo_vehiculo'),
    path('vehiculos/editar/<int:id>/',      views.editar_vehiculo,  name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:id>/',    views.eliminar_vehiculo,name='eliminar_vehiculo'),

    # Empleados
    path('empleados/',                    views.lista_empleados,  name='lista_empleados'),
    path('empleados/nuevo/',              views.nuevo_empleado,   name='nuevo_empleado'),
    path('empleados/editar/<int:id>/',    views.editar_empleado,  name='editar_empleado'),
    path('empleados/eliminar/<int:id>/',  views.eliminar_empleado,name='eliminar_empleado'),

    # Tipos de Servicio
    path('tipos-servicio/',                     views.lista_tipos_servicio,   name='lista_tipos_servicio'),
    path('tipos-servicio/nuevo/',               views.nuevo_tipo_servicio,    name='nuevo_tipo_servicio'),
    path('tipos-servicio/editar/<int:id>/',     views.editar_tipo_servicio,   name='editar_tipo_servicio'),
    path('tipos-servicio/eliminar/<int:id>/',   views.eliminar_tipo_servicio, name='eliminar_tipo_servicio'),

    # Servicios
    path('servicios/',                    views.lista_servicios,  name='lista_servicios'),
    path('servicios/nuevo/',              views.nuevo_servicio,   name='nuevo_servicio'),
    path('servicios/editar/<int:id>/',    views.editar_servicio,  name='editar_servicio'),
    path('servicios/eliminar/<int:id>/',  views.eliminar_servicio,name='eliminar_servicio'),

    # Facturas
    path('facturas/',                   views.lista_facturas,  name='lista_facturas'),
    path('facturas/nueva/',             views.nueva_factura,   name='nueva_factura'),
    path('facturas/detalle/<int:numero>/',  views.detalle_factura, name='detalle_factura'),
    path('facturas/anular/<int:numero>/',   views.anular_factura,  name='anular_factura'),

    path('facturas/ticket/<int:numero>/', views.ticket_factura, name='ticket_factura'),
]


