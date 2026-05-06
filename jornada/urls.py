from django.urls import path
from .views import lista_jornada, inicio_jornada_obligatorio, finalizar_jornada

urlpatterns = [
    path('', lista_jornada, name='lista_jornada'),
    path('inicio/', inicio_jornada_obligatorio, name='inicio_jornada_obligatorio'),
    path('fin/', finalizar_jornada, name='finalizar_jornada'),
]