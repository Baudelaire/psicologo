from django.contrib import admin
from webapp.models import *


class EvaluacionAdmin(admin.ModelAdmin):
    exclude = ('instruciones',)


class PreguntaAdmin(admin.ModelAdmin):
    exclude = ( 'respuesta', 'alternativa_1', 'alternativa_2', 'alternativa_3', 'alternativa_4')


class EvaluadoAdmin(admin.ModelAdmin):
    exclude = ('comentarios', 'fecha')


admin.site.register(Evaluador)
admin.site.register(Evaluado, EvaluadoAdmin)
admin.site.register(Evaluacion, EvaluacionAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
