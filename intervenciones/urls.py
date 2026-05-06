from django.urls import path
from .views import (
    lista_intervenciones,
    lista_clientes,
    detalle_cliente,
    historial_puerta,
    tablero_intervenciones,
)

urlpatterns = [
    path('', lista_intervenciones, name='lista_intervenciones'),
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),
    path('puertas/<int:puerta_id>/historial/', historial_puerta, name='historial_puerta'),
    path('tablero/', tablero_intervenciones, name='tablero_intervenciones'),
]