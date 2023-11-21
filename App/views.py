from django.shortcuts import render,redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.conf import settings
import os
from .forms import *
from .models import *

# Create your views here.
def agregarReserva(request):
    form=FormReserva()
    if request.method == 'POST':
        form = FormReserva(request.POST,request.FILES)#request Files
        if form.is_valid():
            form.save()
            form=FormReserva()
    
    reservas = Reserva.objects.all()
    data={'form':form, 'reservas': reservas}
    return render(request, 'templatesApp/agregar.html',data)

def actualizarReserva(request,id):
    reserva = Reserva.objects.get(idSolicitud=id)
    form = FormReserva(instance=reserva)
    if (request.method == 'POST'):
        form = FormReserva(request.POST,request.FILES,instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    
    reservas=Reserva.objects.all()
    data = {'form':form,'reservas': reservas}
    return render(request, 'templatesApp/agregar.html',data)

def eliminarReserva(request,id):
    reserva = Reserva.objects.get(idSolicitud=id)
    reserva.delete()
    return redirect('/')

def descargar_pdf_reserva(request, id):
    reserva=Reserva.objects.get(idSolicitud=id)
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment;filename="reserva.pdf"'
    p=canvas.Canvas(response)
    p.drawString(100,640, f'Nombre: {reserva.nombre}')
    p.drawString(100,620, f'Telefono: {reserva.telefono}')
    p.drawString(100,600, f'Fecha Reserva: {reserva.fechareserva}')
    p.drawString(100,580, f'Hora Reserva: {reserva.horareserva}')
    p.drawString(100,560, f'Observaciones: {reserva.observaciones}')
    p.drawString(100,540, f'Email: {reserva.email}')
    if reserva.imagenCarnet:
        image_path=os.path.join(settings.MEDIA_ROOT,reserva.imagenCarnet.name)
        if os.path.exists(image_path):
            p.drawImage(image_path,100,660,width=2*inch,height=2*inch)
    p.showPage()
    p.save()
    return response

