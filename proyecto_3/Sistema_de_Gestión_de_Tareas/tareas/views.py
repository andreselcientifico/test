from django.shortcuts import render
from rest_framework import viewsets
from django.urls import reverse_lazy
from .serializer import UserSerializer
from django.views.generic import TemplateView, ListView, DetailView,UpdateView,CreateView
from .models import Tarea

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class CrearTarea(CreateView):
    template_name = 'crear_tarea.html'
    fields = '__all__'
    success_url = '/'
    model = Tarea

    def form_valid(self, form):
        return super().form_valid(form)

class ListaTareas(ListView):
    template_name = 'lista_tareas.html'
    fields = '__all__'
    context_object_name = 'tareas'
    model = Tarea

class DetalleTarea(DetailView):
    template_name = 'detalle_tarea.html'
    fields = '__all__'
    model = Tarea

class EditarTarea(UpdateView):
    template_name = 'editar_tarea.html'
    fields = '__all__'
    model = Tarea

    def get_success_url(self):
        return reverse_lazy('tareas:detalle', kwargs={'pk': self.object.pk})

class EliminarTarea(DetailView):
    template_name = 'eliminar_tarea.html'
    fields = '__all__'
    model = Tarea
    success_url = '/'

class UserViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = UserSerializer