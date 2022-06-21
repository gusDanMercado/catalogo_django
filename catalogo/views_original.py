from ast import Try
from asyncore import read
from faulthandler import disable
from multiprocessing import context
from pyexpat import model
from tkinter import DISABLED
from urllib import request
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.

## desarrollemos el home
from catalogo.models import Autor, Ejemplar, Genero, Idioma, Libro
from django.views import generic

###para trabajar con formularios:
from catalogo.forms import GeneroForm, GeneroForm2, AutorForm
#################################

def index(request):
    #nroAutores = Autor.objects.all().count() ##cuento la cantidad de autores
    ##una forma mas simple de hacer lo anterior es:
    nroAutores = Autor.objects.count() ##ya que el all() esta implicito porque count va a contar todos los objetos(autores) 

    nroEjemplares = Ejemplar.objects.count()
    nroDisponibles = Ejemplar.objects.filter(estado__exact='d').count() ##cuenta la cantidad de ejemplares disponibles

    nroGeneros = Genero.objects.count()
    nroIdiomas = Idioma.objects.count()
    nroLibros = Libro.objects.count()

    ##para renderizar/mostrar esta info, la tenemos que enviar al context, el cual recibe la informacion en 
    ##forma de diccionario de la siguiente manera:
    context = {
        'nroAutores' : nroAutores,
        'nroEjemplares' : nroEjemplares,
        'nroDisponibles' : nroDisponibles,
        'nroGeneros' : nroGeneros,
        'nroIdiomas' : nroIdiomas,
        'nroLibros' : nroLibros,
    }

    ##y este context es el que se envia al render para que el archivo .html lo utilice:
    return render(request, 'index.html', context)

"""
def listaAutores(request):
    autores = Autor.objects.all()  #aqui le digo devolveme todos los autores
    
    context = {
        'autores' : autores,
    }

    return render(request, 'autores.html', context)  
"""

def listaLibros(request):
    libros = Libro.objects.all()

    context = {
        'libros' : libros
    }

    return render(request, 'libros.html', context)

"""
def listaGeneros(request):
    generos = Genero.objects.all()

    context = {
        'generos' : generos
    }

    return render(request, 'generos.html', context)
"""

"""
Lo que hicimos anteriormente fue acceder al modelo y luego llamar al render para pasarlo a una plantilla especifica.

###########################################################################################################################
Otra alternativa seria utilizar una VISTA DE LISTA GENERICA BASADA EN CLASES (ListView), ya que es una vista generica que ya
tiene implementada algunas funcionalidades utiles. Con esto sera mas facil crear una vista y de facil mantenimiento: 
"""

class listaGeneros(generic.ListView):
    model = Genero
    context_object_name = 'generos'
    paginate_by = 2
    template_name = 'generos.html'

#"""
class listaAutores(generic.ListView):
    model = Autor
    context_object_name = 'autores'
    #paginate_by = 2
    template_name = 'autores.html'
#"""

class listaIdiomas(generic.ListView):
    model = Idioma #le paso el nombre del modelo
    context_object_name = 'idiomas' #seria como la variable context
    #template_name = 'idiomas.html'  #nombre del template que va a utilizar
    #queryset= Idioma.objects.all()  #por si quiero filtrar los datos

    ##para utilizar paginacion realizamos:
    paginate_by = 2
    template_name = 'idiomas2.html'


class detalleLibro(generic.DetailView):
    model = Libro
    template_name = 'detalleLibro.html'

    def get_context_data(self, *args, **kwargs):
        libro = Libro.objects.get(pk=self.kwargs['pk'])

        context = super(detalleLibro, self).get_context_data(*args, **kwargs)
        
        # add extra field
        context["ejemplares"] = Ejemplar.objects.filter(libro__pk=libro.pk)
        context["autor"] = Autor.objects.filter(libro__pk=libro.pk)

        return context
    
    def libro_detalle_view(request, pk):
        try:
            libro = Libro.objects.get(pk=pk)
        except Libro.DoesNotExist:
            raise Http404("Ooops! El Libro no existe")
        
        context = {
            'libro' : libro
        }

        return render(request, 'detalleLibro.html', context)
    
class detalleAutor(generic.DetailView):
    model = Autor
    template_name = 'detalleAutor.html'

    def libro_detalle_view(request, pk):
        try:
            autor = Autor.objects.get(pk=pk)
        except Autor.DoesNotExist:
            raise Http404("Ooops! El Autor no existe")
        
        context = {
            'autor' : autor
        }

        return render(request, 'detalleAutor.html', context)

##para realizar el formulario:
################# Genero:
def nuevoGenero(request):
    if request.method == "POST":
        formulario = GeneroForm(request.POST)

        if formulario.is_valid():
            genero = formulario.save(commit=False)
            genero.nombre = formulario.cleaned_data['nombre']
            genero.save()
            return redirect('listaGeneros')
    else:
        formulario = GeneroForm()  #formulario en blanco
    
    return render(request, 'nuevoGenero.html', {'formulario': formulario})

def actualizarGenero(request, pk):
    genero = get_object_or_404(Genero, pk=pk)

    if request.method == "POST":
        formulario = GeneroForm(request.POST, instance=genero)
        if formulario.is_valid():
            genero = formulario.save(commit=False)
            genero.nombre = formulario.cleaned_data['nombre']
            genero.save()
            return redirect('listaGeneros')
    else:
        formulario = GeneroForm(instance=genero)  ##muestro los datos de ese enlace que tiene actualmente el formulario
        
    return render(request, 'nuevoGenero.html', {'formulario': formulario})

def eliminarGenero(request, pk):
    genero = get_object_or_404(Genero , pk = pk)

    if request.method == "POST":
        formulario = GeneroForm2(request.POST, instance=genero)
        if formulario.is_valid():
            genero.delete()
            return redirect('listaGeneros')
    else:
        formulario = GeneroForm2(instance=genero)  
        
    return render(request, 'eliminarGenero.html', {'formulario': formulario})


############### Autor:
def nuevoAutor(request):
    if request.method == "POST":
        formulario = AutorForm(request.POST, request.FILES) ##agrego request.FILES ya que estoy por subir imagenes y con esto le digo que me traiga los archivos file (las imagenes)

        if formulario.is_valid():
            autor = formulario.save(commit=False)
            autor.apenom = formulario.cleaned_data['apenom']
            autor.fechaNac = formulario.cleaned_data['fechaNac']
            autor.fechaDeceso = formulario.cleaned_data['fechaDeceso']
            autor.imagen = formulario.cleaned_data['imagen']

            autor.save()

            return redirect('listaAutores')
    else:
        formulario = AutorForm()

    return render(request, 'nuevoAutor.html', {'formulario' : formulario})


def actualizarAutor(request, pk):
    autor = get_object_or_404(Autor, pk = pk)
    if request.method == "POST":
        formulario = AutorForm(request.POST, request.FILES) 

        if formulario.is_valid():
            autor.apenom = formulario.cleaned_data['apenom']
            autor.fechaNac = formulario.cleaned_data['fechaNac']
            autor.fechaDeceso = formulario.cleaned_data['fechaDeceso']
            autor.imagen = formulario.cleaned_data['imagen']

            autor.save()
            
            return redirect('listaAutores')
    else:
        formulario = AutorForm(instance=autor)
    
    return render(request, 'nuevoAutor.html', { 'formulario' : formulario })