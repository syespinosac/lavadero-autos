from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

     # Clientes
    path('clientes/',                     views.lista_clientes,   name='lista_clientes'),
    path('clientes/nuevo/',               views.nuevo_cliente,    name='nuevo_cliente'),
    path('clientes/editar/<int:id>/',     views.editar_cliente,   name='editar_cliente'),
    path('clientes/eliminar/<int:id>/',   views.eliminar_cliente, name='eliminar_cliente'),
]