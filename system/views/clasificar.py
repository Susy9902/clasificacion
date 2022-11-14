from django.shortcuts import render
import json
from django.http import JsonResponse

from system.services import DB_GlobalService, DB_gruposService
from system.models import DB_global

from django.contrib.auth.decorators import login_required

@login_required
def clasificacion(request):
    return render(request, 'views/CRUDclasificar/clasificacion.html', {
        'items': DB_GlobalService().list(),
        'active': "3"
    })

@login_required
def clasificarBD(request, pk):
    if request.method == 'POST':
        # Extraemos los datos del body que estan en JSON
        data = json.loads(request.body.decode('utf-8'))
        
        service = DB_gruposService()

        if data.get('umbral_tipo') == '-1':
            umbral = float(data.get('umbral'))
        else:
            # Calcular el umbral
            umbral = service.calcular_umbral(pk, data.get('umbral_tipo'))

        # Generar grupos
        result = service.agrupar_matriz(pk, umbral)
        service.clasificar(pk, data.get('criterio'), umbral, 
                           data.get('calculado'), result)

        # Devolver OK o el error
        return JsonResponse({'detail': 'OK'}) if result is not None else JsonResponse({'detail': 'Dara error!'}, status=400)
    return render(request, 'views/CRUDclasificar/clasificarBD.html', {
        'active': "3",
        'pk': pk,
    })

@login_required
def vergrupo(request, pk):
    service = DB_gruposService()
    tabla = service.mostrar_matriz_semajanza(pk)
    grupos = service.mostrar_grupos(pk)
    model = DB_global.objects.get(pk=pk)
    return render(request, 'views/CRUDclasificar/vergrupo.html', {
        'active': "3",
        'pk': pk,
        'tabla': tabla,
        'grupos': grupos,
        'umbral': model.umbral,
    })
