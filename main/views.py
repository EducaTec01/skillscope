from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from .models import Pregunta, Evaluacion, Respuesta
# Create your views here.
# Registro de usuarios
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# Login de usuarios
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Home según el rol
@login_required
def home_view(request):
    if request.user.rol == 'admin':
        preguntas = Pregunta.objects.all()
        return render(request, 'admin_home.html', {'preguntas': preguntas})
    else:
        evaluaciones = Evaluacion.objects.filter(evaluado=request.user)
        return render(request, 'user_home.html', {'evaluaciones': evaluaciones})

# Crear preguntas (solo para admin)
@login_required
def crear_pregunta_view(request):
    if request.user.rol != 'admin':
        return redirect('home')
    if request.method == 'POST':
        texto = request.POST.get('texto')
        competencia_id = request.POST.get('competencia_id')
        Pregunta.objects.create(texto=texto, competencia_id=competencia_id)
        return redirect('home')
    return render(request, 'crear_pregunta.html')

# Responder preguntas (usuario normal)
@login_required
def responder_pregunta_view(request, evaluacion_id):
    evaluacion = Evaluacion.objects.get(id=evaluacion_id)
    if request.method == 'POST':
        for pregunta in evaluacion.preguntas.all():
            puntuacion = request.POST.get(f'puntuacion_{pregunta.id}')
            comentario = request.POST.get(f'comentario_{pregunta.id}')
            Respuesta.objects.create(
                evaluacion=evaluacion,
                pregunta=pregunta,
                evaluador=request.user,
                puntuacion=puntuacion,
                comentario=comentario
            )
        evaluacion.estado = 'completada'
        evaluacion.save()
        return redirect('home')
    preguntas = evaluacion.preguntas.all()
    return render(request, 'responder_preguntas.html', {'preguntas': preguntas})