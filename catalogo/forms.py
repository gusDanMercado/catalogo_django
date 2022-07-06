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
