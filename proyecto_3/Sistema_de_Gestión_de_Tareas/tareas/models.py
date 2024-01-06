from django.db import models

# Create your models here.


class Tarea(models.Model):
    PENDIENTE = 'P'
    EN_PROGRESO = 'E'
    COMPLETADA = 'C'

    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (EN_PROGRESO, 'En Progreso'),
        (COMPLETADA, 'Completada'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.BooleanField(default=False)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=PENDIENTE)

    def __str__(self):
        return self.titulo