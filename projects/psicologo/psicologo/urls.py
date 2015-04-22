from django.conf import settings
from django.conf.urls import patterns, include, url,static
from django.contrib import admin
from webapp.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'psicologo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home/$', HomeViewPersonal.as_view(), name='home_general'),
    url(r'^index/login.html/$', MyLoginView.as_view(), name='login_general'),
    url(r'^finalizado/(?P<id>\d+)/$', HomeViewPersonal.as_view(), name='finalizado_general'),
    url(r'^evaluacion/(?P<id>\d+)/$', EvaluacionView.as_view(), name='evaluacion_general'),
)
if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
