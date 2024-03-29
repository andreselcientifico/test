# Generated by Django 5.0.1 on 2024-01-06 22:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tareas", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tarea",
            name="estado",
            field=models.CharField(
                choices=[("P", "Pendiente"), ("E", "En Progreso"), ("C", "Completada")],
                default="P",
                max_length=1,
            ),
        ),
    ]
