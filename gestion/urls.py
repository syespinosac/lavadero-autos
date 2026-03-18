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
]