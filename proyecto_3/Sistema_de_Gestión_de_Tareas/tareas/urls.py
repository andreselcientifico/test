from django.urls import include
from rest_framework import routers
from django.urls import path
from . import views


router = routers.DefaultRouter()
router.register(r'tareas', views.UserViewSet)

app_name = 'tareas'

urlpatterns = [
    path('',views.HomeView.as_view(), name='Home'),
    path('tareas/',views.CrearTarea.as_view(), name='crear'),
    path('tareas/detalle/<int:pk>',views.DetalleTarea.as_view(), name='detalle'),
    path('tareas/listar/',views.ListaTareas.as_view(), name='lista'),
    path('tareas/editar/<int:pk>',views.EditarTarea.as_view(), name='editar'),
    path('tareas/eliminar/<int:pk>',views.EliminarTarea.as_view(), name='eliminar'),
    path('api/', include(router.urls), name='api'),
]