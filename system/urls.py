from xml.etree.ElementInclude import include
from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView

from system.views import (clasificacion, index, listarDB, ayuda, documentacion, crearBD, detallesBDrasgos, 
                          editarBD, clasificarBD, vergrupo, agregarBDobjetos, listarBDobjetos,
                          modificarBDobjetos, eliminarBD, UserListView, UserDetailView)
from usgest.login import  login_page, logout_view

urlpatterns = [
    # Paginas estaticas
    path('', index, name='home'),
    path('ayuda/', ayuda, name='ayuda'),
    path('documentacion/', documentacion, name='documentacion'),

    # Gestionar DB
    path('listarBD/', listarDB, name='listar_db'),
    path('crearBD/', crearBD, name='crearBD'),
    path('<int:pk>/eliminarBD/', eliminarBD, name='eliminarBD'),
    path('<int:pk>/detallesBDrasgos/', detallesBDrasgos, name='detallesBDrasgos'),
    path('<int:pk>/editarBD/', editarBD, name='editarBD'),

    # Gestionar Objetos de una DB
    path('<int:pk>/agregarBDobjetos/', agregarBDobjetos, name='agregarBDobjetos'),
    path('<int:pk>/listarBDobjetos/', listarBDobjetos, name='listarBDobjetos'),
    path('<int:pk>/modificarBDobjeto/', modificarBDobjetos, name='modificarBDobjeto'),

    # Clasificar DB
    path('clasificacion/', clasificacion, name='clasificacion'),
    path('<int:pk>/clasificarBD/', clasificarBD, name='clasificarBD'),
    path('<int:pk>/vergrupo/', vergrupo, name='vergrupo'),

    #Autenticar
    path('login/', login_page, name='login_page'),
    path('logout_view/', logout_view, name='logout_view'),

    # Gestionar Usuario
    path('listarUsuario/', UserListView.as_view(), name='listarUsuario'),
    path('detalle/<int:pk>/', UserDetailView.as_view(), name='detalle'),
]



