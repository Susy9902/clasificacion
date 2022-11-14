import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from system.services import DB_ObjetosService
from system.models import DB_global

from django.contrib.auth.decorators import login_required

@login_required
def listarBDobjetos(request, pk):
    service = DB_ObjetosService()
    item = get_object_or_404(DB_global, pk=pk)
    data = service.full_detail(pk)
    return render(request, 'views/CRUDobjeto/listarBDobjetos.html', {
        'active': "2",
        'db_item': item,
        'heads': data[0],
        'items': data[1],
    })

@login_required
def modificarBDobjetos(request, pk: int):
    if request.method == 'POST':
        service = DB_ObjetosService()

        # Extraemos los datos del body que estan en JSON
        data = json.loads(request.body.decode('utf-8'))

        # Guardar los datos
        service.add_list(db_global=pk, items=data)

        # Volver a la lista de DB
        return JsonResponse({'detail': 'OK'})
    service = DB_ObjetosService()
    item = get_object_or_404(DB_global, pk=pk)
    data = service.detail(pk)
    rasgos = service.get_rasgos(pk)
    return render(request, 'views/CRUDobjeto/add_edit_BDobjetos.html', {
        'active': "2",
        'pk': pk,
        'db_item': item,
        'heads': data[0],
        'items': data[1],
        'items_rasgos': rasgos,
        'mode': "edit",
    })

@login_required
def agregarBDobjetos(request, pk):
    service = DB_ObjetosService()
    item = get_object_or_404(DB_global, pk=pk)
    data = service.detail(pk)
    rasgos = service.get_rasgos(pk)
    return render(request, 'views/CRUDobjeto/add_edit_BDobjetos.html', {
        'active': "2",
        'pk': pk,
        'db_item': item,
        'heads': data[0],
        'items': data[1],
        'items_rasgos': rasgos,
        'mode': "add",
    })
