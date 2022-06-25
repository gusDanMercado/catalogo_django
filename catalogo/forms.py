from cProfile import label
from dataclasses import field, fields
from email.mime import image
from faulthandler import disable
from msilib.schema import CheckBox
from pyexpat import model
from tkinter import Widget
from django import forms
from catalogo.models import Ejemplar, Genero, Idioma, Autor, Libro
from django.forms.widgets import NumberInput

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ('nombre',)

class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        fields = ('nombre',)

class AutorForm(forms.ModelForm):

    class Meta:
        model = Autor
        fields = ('apenom', 'fechaNac', 'fechaDeceso', 'imagen',)  #

        widgets = {
            'fechaNac' : NumberInput(attrs={ 'type' : 'date' }),
            'fechaDeceso' : NumberInput(attrs={ 'type' : 'date' }),            
        }
    
    ### Para validar formularios utilizaremos la funcion clean, al cual mostrara mensajes de error en la vista correspondiente
    def clean(self):
        super(AutorForm, self).clean()
        fechaNac = self.cleaned_data['fechaNac']
        fechaDeceso = self.cleaned_data['fechaDeceso']
        apenom = self.cleaned_data['apenom']

        #print(fechaNac)
        #print(fechaDeceso)

        if (fechaDeceso!=None and fechaNac!=None):
            if fechaDeceso<fechaNac:
                self.errors['fechaDeceso'] = self.error_class(['La fecha de deceso debe ser mayor a la de nacimiento'])
        
        if len(apenom)<3:
            self.errors['apenom'] = self.error_class(['El apellido debe tener al menos 3 caracteres!!!'])

        return self.cleaned_data

class LibroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LibroForm, self).__init__(*args, **kwargs)
        self.fields['genero'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Genero.objects.all())
    
    class Meta:
        model = Libro
        fields = ('titulo', 'autor', 'resumen', 'genero', 'idioma', 'imagen',)

class crearEjemplarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uniqueId'].disabled = True

    class Meta:
        model = Ejemplar
        fields = ('uniqueId', 'ISBN', 'fechaDevolucion', 'estado', 'libro',)  
        
        widgets = {
            'fechaDevolucion' : NumberInput(attrs={ 'type' : 'date' }),
        }

class editarEjemplarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uniqueId'].disabled = True
        self.fields['ISBN'].disabled = True
        self.fields['libro'].disabled = True

    class Meta:
        model = Ejemplar
        fields = ('uniqueId', 'ISBN', 'fechaDevolucion', 'estado', 'libro',)  
        
        widgets = {
            'fechaDevolucion' : NumberInput(attrs={ 'type' : 'date' }),
        }

class EjemplarForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ##para crear un ejemplar
        self.fields['uniqueId'].widget.attrs.create(disabled = True)     
        #widget.attrs.update
        
        ## para actualizar un ejemplar:
        self.fields['ISBN'].widget.attrs.update(disabled = True)   
        #self.fields['libro'].disabled = True

    class Meta:
        model = Ejemplar
        fields = ('uniqueId', 'ISBN', 'fechaDevolucion', 'estado', 'libro',)  
        
        widgets = {
            'fechaDevolucion' : NumberInput(attrs={ 'type' : 'date' }),
        }
