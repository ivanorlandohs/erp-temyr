from django.db import models
from django.contrib.auth.models import User


class RegistroJornada(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros_jornada')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tecnico.username} - {self.tipo} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"