from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from jornada.models import RegistroJornada


def es_tecnico(user):
    try:
        return user.perfilusuario.rol == 'tecnico'
    except Exception:
        return False


class ControlJornadaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and es_tecnico(request.user):
            hoy = timezone.localdate()

            # Solo de lunes a viernes
            if hoy.weekday() < 5:
                ya_ficho_entrada = RegistroJornada.objects.filter(
                    tecnico=request.user,
                    tipo='entrada',
                    fecha_hora__date=hoy
                ).exists()

                rutas_permitidas = [
                    reverse('login'),
                    reverse('logout'),
                    reverse('inicio_jornada_obligatorio'),
                ]

                if (
                    not ya_ficho_entrada
                    and request.path not in rutas_permitidas
                    and not request.path.startswith('/admin/')
                    and not request.path.startswith('/static/')
                ):
                    return redirect('inicio_jornada_obligatorio')

        response = self.get_response(request)
        return response