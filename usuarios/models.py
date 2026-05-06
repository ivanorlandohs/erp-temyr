from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('tecnico', 'Técnico'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='tecnico')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"