from django.contrib import admin
from .models import RegistroJornada


@admin.register(RegistroJornada)
class RegistroJornadaAdmin(admin.ModelAdmin):
    list_display = ('tecnico', 'tipo', 'fecha_hora')
    list_filter = ('tipo', 'fecha_hora')
    search_fields = ('tecnico__username',)