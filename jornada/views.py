from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import RegistroJornada


def es_tecnico(user):
    try:
        return user.perfilusuario.rol == 'tecnico'
    except Exception:
        return False


@login_required
def inicio_jornada_obligatorio(request):
    hoy = timezone.localdate()

    if hoy.weekday() >= 5:
        return redirect('dashboard')

    ya_ficho_entrada = RegistroJornada.objects.filter(
        tecnico=request.user,
        tipo='entrada',
        fecha_hora__date=hoy
    ).exists()

    if ya_ficho_entrada:
        return redirect('dashboard')

    if request.method == 'POST':
        RegistroJornada.objects.create(
            tecnico=request.user,
            tipo='entrada',
            observaciones='Inicio de jornada registrado desde la app'
        )
        return redirect('dashboard')

    return render(request, 'jornada/inicio_obligatorio.html', {'hoy': hoy})


@login_required
def finalizar_jornada(request):
    hoy = timezone.localdate()

    if request.method == 'POST':
        ya_ficho_salida = RegistroJornada.objects.filter(
            tecnico=request.user,
            tipo='salida',
            fecha_hora__date=hoy
        ).exists()

        if not ya_ficho_salida:
            RegistroJornada.objects.create(
                tecnico=request.user,
                tipo='salida',
                observaciones='Fin de jornada registrado desde la app'
            )

        return redirect('dashboard')

    return render(request, 'jornada/finalizar_jornada.html', {'hoy': hoy})


@login_required
def lista_jornada(request):
    if es_tecnico(request.user):
        registros = RegistroJornada.objects.filter(
            tecnico=request.user
        ).order_by('-fecha_hora')
    else:
        registros = RegistroJornada.objects.all().order_by('-fecha_hora')

    return render(request, 'jornada/lista.html', {'registros': registros})