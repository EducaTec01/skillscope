from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.
# 1. Modelo de usuario extendido para añadir roles
class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('user', 'Usuario Normal'),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default='user')
    # Ajustar los related_name para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_groups',  # Nombre personalizado
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_permissions',  # Nombre personalizado
        blank=True,
        help_text='Permisos específicos del usuario.',
    )

# 2. Competencia (opcional: catalogar por área)
class Competencia(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
# 3. Pregunta vinculada a una competencia
class Pregunta(models.Model):
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto
# 4. Evaluación creada para cada usuario
class Evaluacion(models.Model):
    evaluado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='evaluaciones')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='pendiente')

# 5. Respuesta a las preguntas por el usuario normal
class Respuesta(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)