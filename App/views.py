from django.shortcuts import render,redirect
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