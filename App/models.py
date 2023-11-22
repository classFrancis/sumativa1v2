from django.db import models
from datetime import date

# Create your models here.
class EstadoReserva(models.Model):
    estadoReservaId=models.CharField(primary_key=True,max_length=3)
    estadoReservaNombre=models.CharField(max_length=150)

    def __str__(self):
        return "{}".format(self.estadoReservaNombre)
    
class TipoReserva(models.Model):
    tipoSolicitudId=models.CharField(primary_key=True,max_length=3)
    tipoSolicitud=models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.tipoSolicitud)

class Reserva(models.Model):
    idSolicitud=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50)
    telefono=models.CharField(max_length=12)
    fechaNacimiento=models.DateField()
    fechareserva=models.DateField()
    horareserva=models.TimeField()
    cantidadHermanos=models.IntegerField()
    observaciones=models.CharField(max_length=5000)
    website=models.URLField()
    email=models.EmailField()
    donante=models.BooleanField()
    imagenCarnet=models.ImageField(upload_to='media/')
    codigo_qr=models.ImageField(upload_to='media/',blank=True,null=True)
    F_Creacion=models.DateTimeField()
    F_Modificacion=models.DateTimeField()

    estadoReservaId=models.ForeignKey(EstadoReserva,null=True,blank=False,on_delete=models.RESTRICT)
    tipoSolicitudId=models.ForeignKey(TipoReserva,null=True,blank=False,on_delete=models.RESTRICT)

    def calcular_edad(self):
        fechaActual=date.today()
        fNacimiento=self.fechaNacimiento
        return fechaActual.year - fNacimiento.year - ((fechaActual.month, fechaActual.day) < (fNacimiento.month, fNacimiento.day))