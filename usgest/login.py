from django.shortcuts import render, redirect
from usgest.form import LoginForm, ResgisterForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_page(request):
    message = None
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['usuario']
            password = request.POST['contraseña']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    message = "Te has identificado de modo correcto"
                    return redirect('home')
                else:
             
                   message = "Tu usuario esta inactivo"
            else:
                message = "Nombre de usuario y/o contraseña incorrecto"
    else:
        form = LoginForm()
    return render(request,'login.html', {'form': form, 'message': message})
    
def logout_view(request):
    logout(request)
    return redirect('home')   

def register_view(request): 
    message = None
    if request.method == 'POST':
        form = ResgisterForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username']
            correo = form.cleaned_data['email']
            passw = form.cleaned_data['password']
            nombre = form.cleaned_data['Name']
            apellido = form.cleaned_data['Lastname']
            user_confirm = form.cleaned_data['confirm_password']
            
        if passw == user_confirm:
            user = User.objects.create_user(username=username, email=correo, 
            password= passw, first_name=nombre, last_name = apellido)
            user.save()
            return redirect('login_page')
        else:
            message = 'Las contraseñas no coinciden'
    else:
        form = ResgisterForm()
    return render( request,'register.html', {'form': form, 'message': message},context_instance =RequestContext(request))
    
