from django.shortcuts import render,redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.conf import settings
import os
from io import BytesIO
from django.core.mail import EmailMessage
import qrcode
from django.core.files import File
from io import BytesIO
from .forms import *
from .models import *

#Agregar reserva con qr y foto de carnet
def agregarReserva(request):
    form=FormReserva()
    if request.method == 'POST':
        form = FormReserva(request.POST,request.FILES)#request Files
        if form.is_valid():
            reserva=form.save(commit=False)
            reserva.save()
            reserva.refresh_from_db()
            buffer_qr=generar_qr(reserva)
            nombre_qr=f'codigo_qr_{reserva.idSolicitud}.png'
            reserva.codigo_qr.save(nombre_qr, File(buffer_qr),save=True)

            return redirect('/')
    
    reservas = Reserva.objects.all()
    data={'form':form, 'reservas': reservas}
    return render(request, 'templatesApp/agregar.html',data)

#Actualizar reserva y qr
def actualizarReserva(request,id):
    reserva = Reserva.objects.get(idSolicitud=id)
    form = FormReserva(instance=reserva)
    if (request.method == 'POST'):
        form = FormReserva(request.POST,request.FILES,instance=reserva)
        if form.is_valid():
            reserva=form.save(commit=False)
            if reserva.codigo_qr:
                reserva.codigo_qr.delete(save=False)
            buffer_qr=generar_qr(reserva)
            nombre_qr=f'codigo_qr_{reserva.idSolicitud}.png'
            reserva.codigo_qr.save(nombre_qr, File(buffer_qr),save=True)
            reserva.save()
            reserva.refresh_from_db()
            return redirect('inicio')
    
    reservas=Reserva.objects.all()
    data = {'form':form,'reservas': reservas}
    return render(request, 'templatesApp/agregar.html',data)

def eliminarReserva(request,id):
    reserva = Reserva.objects.get(idSolicitud=id)
    reserva.delete()
    return redirect('/')

# Link de descarga del archivo pdf
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

#Link de guardado temporal en bytes del pdf para enviar por email
def generar_pdf_temporal(reserva):
    buffer=BytesIO()
    p=canvas.Canvas(buffer)
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
    buffer.seek(0)
    return buffer

#Enviar email con reserva
def reserva_email(request):
    if request.method=='POST':
        form=FormReserva(request.POST)
        if form.is_valid():
            reserva=form.save()
            pdf=generar_pdf_temporal(reserva)
            email=EmailMessage(
                'Confirmación de Reserva',
                f'Hola {reserva.nombre}, tu reserva ha sido confirmada. Encuentra adjunto el PDF con los detalles.',
                'tuemaildeapp@gmail.com',
            )
            email.attach('reserva.pdf',pdf.read(),'application/pdf')
            email.send()

            return redirect ('/')
    else:
        form=FormReserva()
        return render(request, 'templatesApp/agregar.html',{'form':form})
    
    return render(request,'templatesApp/agregar.html',{'form':form})

#Generar qr
def generar_qr(reserva):
    datos_qr=str(reserva.idSolicitud)
    qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(datos_qr)
    qr.make(fit=True)
    img=qr.make_image(fill_color='black',back_color='white')

    buffer=BytesIO()
    img.save(buffer)
    buffer.seek(0)

    return buffer


