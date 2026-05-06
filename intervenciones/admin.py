from django.contrib import admin
from .models import Cliente, Puerta, Intervencion


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'municipio')
    search_fields = ('nombre', 'telefono', 'email', 'municipio')


@admin.register(Puerta)
class PuertaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'numero_serie', 'ubicacion', 'marca', 'modelo', 'activa')
    list_filter = ('cliente', 'marca', 'activa')
    search_fields = ('numero_serie', 'ubicacion', 'marca', 'modelo', 'cliente__nombre')


@admin.register(Intervencion)
class IntervencionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'puerta', 'tecnico_asignado', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion', 'puerta__cliente')
    search_fields = (
        'titulo',
        'puerta__numero_serie',
        'puerta__ubicacion',
        'puerta__cliente__nombre',
        'tecnico_asignado__username',
    )