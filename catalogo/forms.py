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

###### para trabajar con el modelo User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
########################################################

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


class UsuarioForm(forms.ModelForm): ## para ver el usuario   

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)  ##estos son los campos que me interesan del usuario (asi figuran en la base de datos)

        ##como yo quiero que los muestre de otra manera en los formularios utilizamos los labels:
        labels = {
            'username' : 'Nombre de Usuario', 
            'first_name' : 'Nombres', 
            'last_name' : 'Apellido', 
            'email' : 'Correo',
        }

class UsuarioForm2(UserCreationForm): ##  para crear el usuario, tuve que usar UserCreationForm ya que este me ayuda automanticamente con la contraseña
    #password1 = forms.CharField(label='Contraseña', help_text="<ul><li>Su contraseña no puede ser demasiado similar a su otra información personal.</li> <li>Su contraseña debe contener al menos 8 caracteres.</li> <li>Su contraseña no puede ser una contraseña de uso común.</li> <li>Su contraseña no puede ser completamente numérica.</li></ul>")
    password2 = forms.CharField(label='Confirme contraseña', help_text="Ingrese la misma contraseña que antes, para verificación.", widget=forms.PasswordInput) # 

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')  ##  estos son los campos que me interesan del usuario (asi figuran en la base de datos)
        ## estos password1 y password2 lo obtuve inspeccionando la pagina desde el navegador

        ##como yo quiero que los muestre de otra manera en los formularios utilizamos los labels:
        labels = {
            'username' : 'Nombre de Usuario', 
            'first_name' : 'Nombres', 
            'last_name' : 'Apellido', 
            'email' : 'Correo',
            #'password1': 'Contraseña',  ##aqui no se porque no me funciono con esto
            #'password2': 'Confirme contraseña'  ##aqui no se porque no me funciono con esto
        }
