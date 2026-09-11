from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('healthz/', views.healthz, name='healthz'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('finance.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('__reload__/', include('django_browser_reload.urls')))
