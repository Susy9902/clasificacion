import json
from pyexpat.errors import messages

from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from system.models import DB_global
from system.services import DB_GlobalService

from django.contrib.auth.decorators import login_required

from usgest.login import login_page, logout_view

@login_required
def listarDB(request):
    return render(request, 'views/CRUDbd/listarBD.html', {
        'items': DB_GlobalService().list(),
        'active': "2"
    })

@login_required
def crearBD(request):
    if request.method == 'POST':
        # Extraemos los datos del body que estan en JSON
        data = json.loads(request.body.decode('utf-8'))

        # Guardar los datos
        service = DB_GlobalService()
        result = service.add(**data)

        # Devolver OK o el error
        return JsonResponse({'detail': 'OK'}) if result is not None else JsonResponse({'detail': 'Dara error!'}, status=400)
    return render(request, 'views/CRUDbd/crearBD.html', {'active': "2"})


def eliminarBD(request, pk: int):
    service = DB_GlobalService()
    service.delete(pk)
    return redirect('listar_db')

@login_required
def detallesBDrasgos(request, pk: int):
    item = get_object_or_404(DB_global, pk=pk)
    return render(request, 'views/CRUDbd/detallesBDrasgos.html', {
        'rasgos': DB_GlobalService().detail(pk),
        'item': item,
        'active': "2"
    })

@login_required
def editarBD(request, pk: int):
    service = DB_GlobalService()
    obj = get_object_or_404(DB_global, pk=pk)
    if request.method == 'POST':
        # Extraemos los datos del body que estan en JSON
        data = json.loads(request.body.decode('utf-8'))

        # Guardar los datos
        result = service.edit(pk=pk, **data)

        # Volver a la lista de DB
        return JsonResponse({'detail': 'OK'}) if result is not None else JsonResponse({'detail': 'Dara error!'}, status=400)
    return render(request, 'views/CRUDbd/editarBD.html', 
    {'active': "2", 'item': obj, 'rasgos': service.detail_modificar(pk)})


