from django.test import TestCase
from .models import Tarea
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your tests here.
class TareaModelTest(TestCase):

    def setUp(self):
        self.tarea = Tarea.objects.create(titulo='Prueba', descripcion='Descripción de prueba', estado=Tarea.PENDIENTE)
        self.tarea1 = Tarea.objects.create(titulo='Prueba', descripcion='Descripción de prueba', estado=Tarea.EN_PROGRESO)
        self.tarea2 = Tarea.objects.create(titulo='Prueba', descripcion='Descripción de prueba', estado=Tarea.COMPLETADA)

    def test_tarea_str_method(self):
        self.assertEqual(str(self.tarea), 'Prueba')
        self.assertEqual(str(self.tarea1), 'Prueba')
        self.assertEqual(str(self.tarea2), 'Prueba')


class TareaViewsTest(TestCase):

    def test_home_view_status_code(self):
        response = self.client.get(reverse('tareas:Home'))
        self.assertEqual(response.status_code, 200)

    def test_crear_tarea_view_status_code(self):
        response = self.client.get(reverse('tareas:crear'))
        self.assertEqual(response.status_code, 200)

    def test_detalle_tarea_view_status_code(self):
        # Crea una tarea para ver sus detalles
        tarea = Tarea.objects.create(titulo='Tarea a Detallar', descripcion='Descripción de prueba', estado=Tarea.PENDIENTE)

        # Obtiene la URL para ver los detalles de la tarea recién creada
        url = reverse('tareas:detalle', args=[tarea.pk])

        # Realiza la solicitud GET a la vista de detalles
        response = self.client.get(url)

        # Verifica que la respuesta sea 200 (OK) al intentar ver los detalles de la tarea
        self.assertEqual(response.status_code, 200)

    def test_eliminar_tarea_view_status_code(self):
        tarea = Tarea.objects.create(titulo='Tarea a Eliminar', descripcion='Descripción de prueba', estado=Tarea.PENDIENTE)
        url = reverse('tareas:eliminar', args=[tarea.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Verificar la redirección después de la eliminación
