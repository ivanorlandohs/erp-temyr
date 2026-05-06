from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Puerta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='puertas')
    codigo = models.CharField(max_length=50, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=255)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.ubicacion} - {self.numero_serie}"


class Intervencion(models.Model):
    ESTADO_CHOICES = [
        ('averia', 'Avería'),
        ('en_proceso', 'En proceso'),
        ('finalizada', 'Finalizada'),
        ('parte_entregado', 'Parte entregado'),
    ]

    puerta = models.ForeignKey(
        Puerta,
        on_delete=models.CASCADE,
        related_name='intervenciones',
        null=True,
        blank=True
    )
    tecnico_asignado = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='intervenciones_asignadas'
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    trabajo_realizado = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='averia')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.puerta:
            return f"{self.titulo} - {self.puerta.numero_serie}"
        return f"{self.titulo} - Sin puerta"