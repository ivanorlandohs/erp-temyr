from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Cliente, Puerta, Intervencion


def es_tecnico(user):
    try:
        return user.perfilusuario.rol == 'tecnico'
    except Exception:
        return False


@login_required
def lista_intervenciones(request):
    intervenciones = Intervencion.objects.select_related(
        'puerta', 'puerta__cliente', 'tecnico_asignado'
    )

    if es_tecnico(request.user):
        intervenciones = intervenciones.filter(tecnico_asignado=request.user)

    intervenciones = intervenciones.order_by('-fecha_creacion')

    return render(request, 'intervenciones/lista.html', {'intervenciones': intervenciones})


@login_required
def lista_clientes(request):
    if es_tecnico(request.user):
        clientes = Cliente.objects.filter(
            puertas__intervenciones__tecnico_asignado=request.user
        ).distinct().order_by('nombre')
    else:
        clientes = Cliente.objects.all().order_by('nombre')

    return render(request, 'intervenciones/clientes.html', {'clientes': clientes})


@login_required
def detalle_cliente(request, cliente_id):
    if es_tecnico(request.user):
        cliente = get_object_or_404(
            Cliente.objects.filter(
                puertas__intervenciones__tecnico_asignado=request.user
            ).distinct(),
            id=cliente_id
        )
        puertas = cliente.puertas.filter(
            intervenciones__tecnico_asignado=request.user
        ).distinct().order_by('ubicacion')
    else:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        puertas = cliente.puertas.all().order_by('ubicacion')

    return render(request, 'intervenciones/detalle_cliente.html', {
        'cliente': cliente,
        'puertas': puertas,
    })


@login_required
def historial_puerta(request, puerta_id):
    if es_tecnico(request.user):
        puerta = get_object_or_404(
            Puerta.objects.filter(
                intervenciones__tecnico_asignado=request.user
            ).distinct(),
            id=puerta_id
        )
    else:
        puerta = get_object_or_404(Puerta, id=puerta_id)

    historial = puerta.intervenciones.select_related(
        'tecnico_asignado'
    ).all().order_by('-fecha_creacion')

    return render(request, 'intervenciones/historial_puerta.html', {
        'puerta': puerta,
        'historial': historial,
    })


@login_required
def tablero_intervenciones(request):
    clientes = Cliente.objects.all().order_by('nombre')
    cliente_id = request.GET.get('cliente')

    intervenciones = Intervencion.objects.select_related(
        'puerta', 'puerta__cliente', 'tecnico_asignado'
    ).all()

    if es_tecnico(request.user):
        intervenciones = intervenciones.filter(tecnico_asignado=request.user)
        clientes = Cliente.objects.filter(
            puertas__intervenciones__tecnico_asignado=request.user
        ).distinct().order_by('nombre')

    if cliente_id:
        intervenciones = intervenciones.filter(puerta__cliente_id=cliente_id)

    averias = intervenciones.filter(estado='averia').order_by('-fecha_creacion')
    en_proceso = intervenciones.filter(estado='en_proceso').order_by('-fecha_creacion')
    finalizadas = intervenciones.filter(estado='finalizada').order_by('-fecha_creacion')
    partes_entregados = intervenciones.filter(estado='parte_entregado').order_by('-fecha_creacion')

    return render(request, 'intervenciones/tablero.html', {
        'clientes': clientes,
        'cliente_id': cliente_id,
        'averias': averias,
        'en_proceso': en_proceso,
        'finalizadas': finalizadas,
        'partes_entregados': partes_entregados,
    })