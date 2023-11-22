"""
URL configuration for sumativa1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.agregarReserva, name='inicio'),
    path('eliminar/<int:id>',views.eliminarReserva, name='eliminar_reserva'),
    path('actualizar/<int:id>',views.actualizarReserva, name='actualizar_reserva'),
    path('reserva/<int:id>/pdf/', views.descargar_pdf_reserva, name='descargar_pdf_reserva'),
    path('enviar_reserva/', views.reserva_email, name='reserva_email'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

