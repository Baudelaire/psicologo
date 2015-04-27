# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Evaluador(models.Model):
    evaluador = models.ForeignKey(User, related_name='evaluador')
    nombres = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    codigo = models.CharField(max_length=8)

    def __unicode__(self):
        return u'{0} {1} {2}'.format(self.nombres, self.apellido_paterno,
                                     self.apellido_materno)


class Evaluado(models.Model):
    nombres = models.CharField(max_length=25)
    apellido_paterno = models.CharField(max_length=15)
    apellido_materno = models.CharField(max_length=15)
    codigo = models.CharField(max_length=8)
    evaluador = models.ForeignKey(Evaluador, related_name='evaluadores')
    CATEGORIA_CHOICES = (
                            ("1", "categoria 1"),
                            ("2", "categoria 2"),
                            ("3", "categoria 3"),
                            ("4", "categoria 4"),
    )
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    comentarios = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    estado = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return u'{0} {1} {2}'.format(self.nombres, self.apellido_paterno,
                                     self.apellido_materno)


class Evaluacion(models.Model):
    CATEGORIA_CHOICES = (
                            ("1", "categoria 1"),
                            ("2", "categoria 2"),
                            ("3", "categoria 3"),
                            ("4", "categoria 4"),
    )
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    instruciones = models.TextField()

    def __unicode__(self):
        return u'{0}'.format(self.categoria)


class Pregunta(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, related_name='ev_pregunta')
    AREA_CHOICES = (("CUMPLIMIENTO DE PLAZOS", "CUMPLIMIENTO DE PLAZOS"),
                    ("CALIDAD DE PROCESOS Y PRODUCTOS",
                        "CALIDAD DE PROCESOS Y PRODUCTOS"),
                    ("IMPACTO O RELEVANCIA", "IMPACTO O RELEVANCIA"))
    area = models.CharField(max_length=35, choices=AREA_CHOICES)
    enunciado = models.TextField()
    ALTERNATIVA_CHOICES = (
                            ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")
                        )
    # QUITAR DEL ADMIN CON ALTERNATIVAS Y RESPUESTA
    respuesta = models.CharField(blank=True, null=True,
                                 choices=ALTERNATIVA_CHOICES, max_length=1)
    alternativa_1 = models.CharField(blank=True, null=True, max_length=30,
                                     default='Excede las espectativas')
    alternativa_2 = models.CharField(blank=True, null=True, max_length=30,
                                     default='Frecuentemente cumple')
    alternativa_3 = models.CharField(blank=True, null=True, max_length=30,
                                     default='Algunas veces cumple')
    alternativa_4 = models.CharField(blank=True, null=True, max_length=30,
                                     default='Nunca cumple')

    def __unicode__(self):
        return u'{0} - {1}'.format(self.area, self.evaluacion)


class Respuesta(models.Model):
    evaluado = models.ForeignKey(Evaluado, related_name='re_evaluado')
    evaluador = models.ForeignKey(Evaluador, related_name='re_evaluador')
    pregunta = models.ForeignKey(Pregunta, related_name='re_pregunta')
    alternativa = models.CharField(blank=True, null=True, max_length=1)

    class Meta:
        unique_together = (('evaluado', 'pregunta'))
