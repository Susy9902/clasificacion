from django import views
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.views.generic import DetailView

class UserListView(ListView):
    model = User
    template_name = 'views/CRUDusuario/listarUsuario.html'

class UserDetailView(DetailView):
    model = User
    template_name = 'views/CRUDusuario/detalle.html'