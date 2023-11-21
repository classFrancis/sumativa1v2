from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from App.models import *

class FormReserva(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        exclude = ['F_Modificacion']

    ESTADOS_CHOICE=(
        ('guardado','GUARDADO'),
        ('anulado','ANULADO'),
        ('confirmado','CONFIRMADO'),
    )
    
    fechareserva=forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'date'}),label='Fecha Reserva')
    horareserva=forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type':'time','fromat':'%H:%M'}),label='Hora Reserva')
    observaciones=forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':50}))

    estadoReservaId=forms.ModelChoiceField(queryset=EstadoReserva.objects.all(),label='Estado Reserva')
    estadoReservaId.widget.attrs['class']='form-select'

    imagenCarnet=forms.ImageField(label='Imagen Carnet')
    
    tipoSolicitudId=forms.ModelChoiceField(queryset=TipoReserva.objects.all(),label='Tipo Reserva')
    tipoSolicitudId.widget.attrs['class']='form-select'

    def clean_edad(self):
        edad=self.cleaned_data.get('edad')
        if edad <18:
            raise forms.ValidationError('Debe ser mayor de edad')
        return edad

    def clean_nombre(self):
        nombre=self.cleaned_data.get('nombre')
        if len(nombre) <=2:
            raise forms.ValidationError('El nombre debe contener mas de dos letras')
        return nombre
    
    def clean_observaciones(self):
        observaciones=self.cleaned_data.get('observaciones')
        palabras=observaciones.split()

        if len(palabras)<5:
            raise forms.ValidationError('Las observaciones deben contener almenos 5 palabras')
        return observaciones
    