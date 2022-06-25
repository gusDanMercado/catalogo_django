from asyncio.windows_events import NULL
from enum import auto
from logging import raiseExceptions
from multiprocessing import context
from select import select
from django.shortcuts import render, redirect, get_object_or_404
from catalogo.models import Autor, Genero, Idioma, Libro, Ejemplar, POI

from django.views import generic
from catalogo.forms import GeneroForm, IdiomaForm, AutorForm, LibroForm, crearEjemplarForm, editarEjemplarForm, EjemplarForm

from django.http import Http404

import os

### para los graficos:
import random
from random import randint

### para los Mapas:
import json
from django.core.serializers import serialize
from django.views.generic.base import TemplateView

###################################### index o Pagina Principal (Home) ###############################################
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

######################################################################################################################

####################################### GENERO #######################################################################

## Para ver todos los generos:
"""
def listaGeneros(request):
    generos = Genero.objects.all()

    context = {
        'generos' : generos
    }

    return render(request, 'generos.html', context)


Luego, podemos hacer esto usando ListView:
"""
class listaGeneros(generic.ListView):
    model = Genero
    context_object_name = 'generos'
    paginate_by = 2
    template_name = 'generos.html'

## Para ver un Genero:
class detalleGenero(generic.DetailView):
    model = Genero
    template_name = 'detalleGenero.html'

    def genero_detalle_view(request, pk):
        try:
            genero = Genero.objects.get(pk=pk)
        except Genero.DoesNotExist:
            raise Http404("Ooops! El Genero no existe")
        
        context = {
            'genero' : genero
        }

        return render(request, 'detalleGenero.html', context)

## Para crear un nuevo genero:
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

## Para actualizar un genero
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

## Para eliminar un genero especifico
"""
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

Una mejor, manera de realizar esta eliminacion evitando ir a otra pagina, es utilizando MODALES,
de la siguiente manera:
"""
def eliminarGenero(request, pk):
    genero = get_object_or_404(Genero, pk = pk)
    genero.delete()
    return redirect('listaGeneros')

######################################################################################################################


####################################### IDIOMA #######################################################################
## Para ver todos los idiomas:
class listaIdiomas(generic.ListView):
    model = Idioma
    context_object_name = 'idiomas'
    paginate_by = 2
    template_name = 'idiomas.html'

## Para ver un idioma:
class detalleIdioma(generic.DetailView):
    model = Idioma
    template_name = 'detalleIdioma.html'

    def idioma_detalle_view(request, pk):
        try:
            idioma = Idioma.objects.get(pk = pk)
        except Idioma.DoesNotExist:
            raise Http404("Ooops! El Genero no existe")
        
        context = {
            'idioma' : 'idioma'
        }

        return render(request, 'detalleIdioma.html', context)

## Para crear un nuevo idioma:
def nuevoIdioma(request):
    if request.method == "POST":
        formulario = IdiomaForm(request.POST)

        if formulario.is_valid():
            idioma = formulario.save(commit=False)
            idioma.nombre = formulario.cleaned_data['nombre']
            idioma.save()

            return redirect('listaIdiomas')
    else:
        formulario = IdiomaForm()
    
    return render(request, 'nuevoIdioma.html', { 'formulario' : formulario })

## Para actualizar un idioma:
def actualizarIdioma(request, pk):
    idioma = get_object_or_404(Idioma, pk = pk)

    if request.method == "POST":
        formulario = IdiomaForm(request.POST, instance=idioma)

        if formulario.is_valid():
            idioma = formulario.save(commit=False)
            idioma.nombre = formulario.cleaned_data['nombre']
            idioma.save()

            return redirect('listaIdiomas')
    else:
        formulario = IdiomaForm(instance=idioma)

    return render(request, 'nuevoIdioma.html', { 'formulario' : formulario })    
    
## Para eliminar un idioma especifico
def elimanarIdioma(request, pk):
    idioma = get_object_or_404(Idioma, pk = pk)
    idioma.delete()
    return redirect('listaIdiomas')

######################################################################################################################


####################################### AUTOR ########################################################################
## Para ver todos los autores:
class listaAutores(generic.ListView):
    model = Autor
    context_object_name = 'autores'
    paginate_by = 2
    template_name = 'autores.html'

## Para ver un autor:
class detalleAutor(generic.DetailView):
    model = Autor
    template_name = 'detalleAutor.html'

    def autor_detalle_view(request, pk):
        try:
            autor = Autor.objects.get(pk = pk)
        except Autor.DoesNotExist:
            raise Http404("Ooops! El Autor no existe")

        context = {
            'autor' : autor
        }

        return render(request, 'detalleAutor.html', context)

## Para crear un nuevo autor:
def nuevoAutor(request):
    if request.method == "POST":
        formulario = AutorForm(request.POST, request.FILES)

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
    
    return render(request, 'nuevoAutor.html', { 'formulario' : formulario })

## Para actualizar un autor:
def actualizarAutor(request, pk):
    autor = get_object_or_404(Autor, pk = pk)

    if request.method == "POST":
        formulario = AutorForm(request.POST, request.FILES, instance=autor) 

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

## Para eliminar un autor especifico
def eliminarAutor(request, pk):
    autor = get_object_or_404(Autor, pk = pk)

    ### para eliminar la imagen de mi directorio
    #print("La direccion de mi imagen es: ",autor.imagen.path)
    #print("dir name: ", os.path.dirname(autor.imagen.path))

    if os.path.isfile(autor.imagen.path) and os.path.dirname(autor.imagen.path)!='E:\DesarrolloWeb2022\Django\Proyecto2\media\img':
        os.remove(autor.imagen.path)
    
    autor.delete()
    return redirect('listaAutores')

######################################################################################################################


####################################### LIBRO ########################################################################
## Para ver todos los libros:
class listaLibros(generic.ListView):
    model = Libro
    context_object_name = 'libros'
    paginate_by = 2
    template_name = 'libros.html'

## Para ver un libro:
class detalleLibro(generic.DetailView):
    model = Libro
    template_name = 'detalleLibro.html'

    def get_context_data(self, *args, **kwargs):   ##en caso de que necesite datos de este libro que se encuentren en otro modelo
        libro = Libro.objects.get(pk=self.kwargs['pk'])

        context = super(detalleLibro, self).get_context_data(*args, **kwargs)
        
        # add extra field
        context["ejemplares"] = Ejemplar.objects.filter(libro__pk=libro.pk)

        return context

    def libro_detalle_view(request, pk):
        try:
            libro = Libro.objects.get(pk = pk)
        except Libro.DoesNotExist:
            raise Http404("Ooops! El Autor no existe")
        
        context = {
            'libro' : libro
        }

        return render(request, 'detalleLibro.html', context)

## Para crear un nuevo libro:
def nuevoLibro(request):
    if request.method == "POST":
        formulario = LibroForm(request.POST, request.FILES)

        if formulario.is_valid():
            libro = formulario.save(commit=False)

            libro.titulo = formulario.cleaned_data['titulo']
            libro.autor = formulario.cleaned_data['autor']
            libro.resumen = formulario.cleaned_data['resumen']
            #libro.genero = formulario.cleaned_data['genero']  ##(No funciona porque es una relacion de muchos a muchos)          
            libro.idioma = formulario.cleaned_data['idioma']
            libro.imagen = formulario.cleaned_data['imagen']

            #print("La ruta de mi imagen es: ", libro.imagen.path)

            libro.save()

            ## para solucionar esto realizamos (el tema de genero):
            for genero in formulario.cleaned_data['genero']:
                #print(genero)
                if genero!=None:
                    libro.genero.add(genero)
            
            #print("La ruta de mi imagen es: ", libro.imagen.path)
            
            return redirect('listaLibros')
    else:
        formulario = LibroForm()
    
    return render(request, 'nuevolibro.html', { 'formulario' : formulario })

## Para actualizar un libro:   
def actualizarLibro(request, pk):
    libro = get_object_or_404(Libro, pk = pk)

    if request.method == "POST":
        formulario = LibroForm(request.POST, request.FILES, instance=libro) 

        if formulario.is_valid():
            libro.titulo = formulario.cleaned_data['titulo']
            libro.autor = formulario.cleaned_data['autor']
            libro.resumen = formulario.cleaned_data['resumen']
            #libro.genero = formulario.cleaned_data['genero']  ##(No funciona porque es una relacion de muchos a muchos)          
            libro.idioma = formulario.cleaned_data['idioma']
            libro.imagen = formulario.cleaned_data['imagen']

            ## para solucionar esto realizamos (el tema de genero):
            for element in libro.genero.all(): ##eliminamos todos los generos, para luego cargar los nuevos, sino hacemos esto los generos que destildemos no se van a destildar
                print(element)
                if element!=None:
                    libro.genero.remove(element)

            libro.save()

            ## ahora cargamos los nuevos generos:
            for genero in formulario.cleaned_data['genero']:
                print(genero)
                if genero!=None:
                    libro.genero.add(genero)
            
            return redirect('listaLibros')
    else:
        formulario = LibroForm(instance=libro)
    
    return render(request, 'nuevoLibro.html', { 'formulario' : formulario })

## Para eliminar un libro especifico
def eliminarLibro(request, pk):
    libro = get_object_or_404(Libro, pk = pk)

    print("La direccion de la imagen es: ",libro.imagen.path)

    ### para eliminar la imagen de mi directorio
    if os.path.isfile(libro.imagen.path) and os.path.dirname(libro.imagen.path)!='E:\DesarrolloWeb2022\Django\Proyecto2\media\img':
        os.remove(libro.imagen.path)

    libro.delete()
    return redirect('listaLibros')

######################################################################################################################


####################################### EJEMPLAR #####################################################################
## Para ver todos los ejemplares:
class listaEjemplares(generic.ListView):
    model = Ejemplar
    context_object_name = 'ejemplares'
    paginate_by = 2
    template_name = 'ejemplares.html'

## Para ver un ejemplar:
class detalleEjemplar(generic.DetailView):
    model = Ejemplar
    template_name = 'detalleEjemplar.html'

    def ejemplar_detalle_view(request, pk):
        try:
            ejemplar = Ejemplar.objects.get(pk = pk)
        except Ejemplar.DoesNotExist:
            raise Http404("Ooops! El Ejemplar no existe")
        
        context = {
            'ejemplar' : ejemplar
        }

        return render(request, 'detalleEjemplar.html', context)

## Para crear un nuevo ejemplar:
def nuevoEjemplar(request):
    if request.method == "POST":
        formulario = crearEjemplarForm(request.POST)  #crear

        if formulario.is_valid():
            ejemplar = formulario.save(commit=False)
     
            ejemplar.uniqueId = formulario.cleaned_data['uniqueId']
            ejemplar.ISBN = formulario.cleaned_data['ISBN']
            ejemplar.fechaDevolucion = formulario.cleaned_data['fechaDevolucion']
            ejemplar.estado = formulario.cleaned_data['estado']
            ejemplar.libro = formulario.cleaned_data['libro']

            ejemplar.save()
            return redirect('listaEjemplares')
    else:
        formulario = crearEjemplarForm()  #crear
    
    return render(request, 'nuevoEjemplar.html', { 'formulario' : formulario })

## Para actualizar un libro: 
def actualizarEjemplar(request, pk):
    ejemplar = get_object_or_404(Ejemplar, pk = pk)

    if request.method == "POST":
        formulario = editarEjemplarForm(request.POST, instance=ejemplar)   #editar

        if formulario.is_valid():

            ejemplar.uniqueId = formulario.cleaned_data['uniqueId']
            ejemplar.ISBN = formulario.cleaned_data['ISBN']   ##hacer el isbn disable cuando este por actualizar y el libro tambien
            ejemplar.fechaDevolucion = formulario.cleaned_data['fechaDevolucion']
            ejemplar.estado = formulario.cleaned_data['estado']
            ejemplar.libro = formulario.cleaned_data['libro']

            ejemplar.save()
            
            return redirect('listaEjemplares')
    else:
        formulario = editarEjemplarForm(instance=ejemplar)  #editar
    
    return render(request, 'nuevoEjemplar.html', { 'formulario' : formulario })

## Para eliminar un ejemplar especifico
def eliminarEjemplar(request, pk):
    ejemplar = get_object_or_404(Ejemplar, pk = pk)
    ejemplar.delete()
    return redirect('listaEjemplares')

######################################################################################################################


####################################### GRAFICOS #####################################################################

def chartData(request):
    chartLabel = "Prestamos"
    etiquetas = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    meses = 12
    minimo = 10
    maximo = 100

    datos = []

    for i in range(meses):
        datos.append(randint(minimo, maximo))

    context = {
        "labels":etiquetas,
        "chartLabel":chartLabel, 
        "data":datos,
    }

    return render(request, 'charts.html', context)


######################################################################################################################


####################################### MAPAS ########################################################################
class POIsMapView(TemplateView):
    ###POIS and map view.
    template_name = "map.html"
    def get_context_data(self, **kwargs):
        ###Return the view context data.
        context = super().get_context_data(**kwargs)
        pois = POI.objects.all()
        lista=[]
        for poi in pois:
            json_dict={}
            json_dict['type'] = 'Feature'
            json_dict['properties'] = dict(name=poi.nombre)
            json_dict['geometry'] = dict(type='Point', coordinates=list([poi.lng ,poi.lat]))
            lista.append(json_dict)
          
        context["markers"]= lista

        return context
 
######################################################################################################################