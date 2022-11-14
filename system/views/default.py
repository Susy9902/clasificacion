from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def documentacion(request):
    return render(request, 'views/database/documentacion.html', {
        'active': "1"
    })

@login_required
def ayuda(request):
    return render(request, 'views/database/ayuda.html', {
        'active': "4"
    })


@login_required
def index(request):
    return render(request, 'views/index.html', {
        'active': "0"
    })
