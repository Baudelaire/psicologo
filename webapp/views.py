# -*- encoding: utf-8 -*-
from class_based_auth_views.views import LoginView
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from webapp.models import *


class IndexView(TemplateView):
    template_name = 'index.html'


class MyLoginView(LoginView):
    template_name = 'login.html'
    success_url = "/home/"

    def form_valid(self, form):
        if Group.objects.filter(Q(user__username__in=(form.cleaned_data["username"],), name="evaluadores") | Q(
                user__username__in=(form.cleaned_data["username"],), name="administradores")):
            return super(MyLoginView, self).form_valid(form)
        messages.warning(self.request, "No perteneces a ningun grupo")
        return self.form_invalid(form)


class HomeViewPersonal(TemplateView):
    def get_template_names(self):
        if Group.objects.filter(user__in=(self.request.user,), name="evaluadores"):
            return ['evaluador.html']
        elif Group.objects.filter(user__in=(self.request.user,), name="administradores"):
            return ['home_administrador.html']

    def get_context_data(self, **kwargs):
        if Group.objects.filter(user__in=(self.request.user,), name="evaluadores"):
            usuario = self.request.user
            evaluador = usuario.evaluador.all().filter(evaluador=usuario)
            evaluados = Evaluado.objects.all().filter(evaluador=evaluador)
            return {'evaluados': evaluados, 'evaluador': evaluador}

        elif Group.objects.filter(user__in=(self.request.user,), name="jefes"):
            jefe = self.request.user
            prueba = jefe.jefe_pruebas.all()
            for pru in prueba:
                usuarios = pru.usuario.all()
            return {'jefe': jefe, 'usuarios': usuarios}

    def post(self, request, *args, **kwargs):
        template_name = 'evaluador.html'
        usuario = self.request.user
        evaluador = Evaluador.objects.all().get(evaluador=usuario)
        evaluados = Evaluado.objects.all().filter(evaluador=evaluador)
        id = self.kwargs['id']
        #usuario.is_active = False
        llaves = self.request.POST.keys()
        evaluado = Evaluado.objects.all().get(id=id)
        evaluacion = Evaluacion.objects.all().get(categoria=evaluado.categoria)
        preguntas = evaluacion.ev_pregunta.all()
        for pregunta in preguntas:
            for llave in llaves:
                llave_c = llave
                if llave == 'fecha':
                    print self.request.POST[llave]
                    #evaluado.fecha = self.request.POST[llave]
                if llave == 'comentarios':
                    evaluado.comentarios = self.request.POST[llave]
                if llave != 'csrfmiddlewaretoken' and llave != 'fecha' and llave != 'comentarios':
                    llave_c = int(llave)
                if llave_c == pregunta.id:
                    Respuesta.objects.get_or_create(evaluado=evaluado, pregunta=pregunta, evaluador=evaluador,
                                                    alternativa=self.request.POST[llave])
        evaluado.save()
        return render(self.request, template_name, {'evaluados': evaluados, 'evaluador': evaluador})


class EvaluacionView(TemplateView):
    template_name = 'evaluacion.html'

    def get_context_data(self, **kwargs):
        id = self.kwargs['id']
        evaluado = Evaluado.objects.get(id=id)
        usuario = self.request.user
        evaluador = usuario.evaluador.all().filter(evaluador=usuario)
        evaluacion = Evaluacion.objects.get(categoria=evaluado.categoria)
        preguntas = evaluacion.ev_pregunta.all()
        fecha = datetime.now()
        return {'evaluado': evaluado, 'evaluador': evaluador, 'evaluacion': evaluacion, 'preguntas': preguntas,
                'fecha': fecha}
