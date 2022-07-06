from asyncio.windows_events import NULL
from enum import auto
from logging import raiseExceptions
from multiprocessing import context
from pickle import UNICODE
from select import select
from urllib import response
from xml.dom import xmlbuilder
from django import views
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from catalogo.models import Autor, Genero, Idioma, Libro, Ejemplar, POI

from django.views import View, generic
from catalogo.forms import GeneroForm, IdiomaForm, AutorForm, LibroForm, crearEjemplarForm, editarEjemplarForm, EjemplarForm

from django.http import Http404, HttpResponse, HttpResponseRedirect

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
    if os.path.isfile(autor.imagen.path):
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

            libro.save()

            ## para solucionar esto realizamos (el tema de genero):
            for genero in formulario.cleaned_data['genero']:
                #print(genero)
                if genero!=None:
                    libro.genero.add(genero)
            
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

    ### para eliminar la imagen de mi directorio
    if os.path.isfile(libro.imagen.path):
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
            json_dict['geometry'] = dict(type='Point', coordinates=list([poi.longitude,poi.latitude]))
            lista.append(json_dict)
        
        context["markers"]= lista

        return context
 
######################################################################################################################


############################################ PUNTOS ##################################################################
## Para ver todos los puntos:
class listaPuntos(generic.ListView):
    model = POI
    context_object_name = 'puntos'
    paginate_by = 2
    template_name = 'puntos.html'

## Para ver un punto:
class detallePunto(generic.DetailView):
    model = POI
    template_name = 'detallePunto.html'

    def punto_detalle_view(request, pk):
        try:
            punto = POI.objects.get(pk = pk)
        except POI.DoesNotExist:
            raise Http404("Ooops! El Punto no existe")

        context = {
            'punto' : punto
        }

        return render(request, 'detallePunto.html', context)


class listaPuntos_3(generic.ListView):
    model = POI
    context_object_name = 'punto'
    paginate_by = 2
    template_name = 'showmap.html' ##'puntos.html'


class listaPuntos_2(generic.ListView):
    model = POI
    context_object_name = 'puntos'
    #paginate_by = 2
    template_name = 'showroute.html' ##'puntos.html'


### reportes:
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

class PDFAutores(View):

    def get(self, request, *args, **kwargs):

        try:
            template = get_template('reporteautores.html')

            context = {
                'title' : 'Lista de Autores',
                'autores' : Autor.objects.all(),
                'totalAut' : Autor.objects.count(),
                'title2' : 'Lista de Libros',
                'libros' : Libro.objects.all(),
                'totalLib' : Libro.objects.count(),
                'title3' : 'Lista de Ejemplares',
                'ejemplares' : Ejemplar.objects.all(), 
                'cantEjemplarDisponibles' : Ejemplar.objects.filter(estado__exact='d').count(),
                'cantEjemplarPrestados' : Ejemplar.objects.filter(estado__exact='p').count(),
                'cantEjemplarMant' : Ejemplar.objects.filter(estado__exact='m').count(),
                'cantEjemplarReserv' : Ejemplar.objects.filter(estado__exact='r').count(),
                'totalEje' : Ejemplar.objects.count()
            }

            html = template.render(context)

            response = HttpResponse() ##context_type = 'application/pdf'
            response['Content-Disposition'] = 'attachment; filename="autores.pdf"'  ##   esta opcion hace que se me descarge el archivo

            ##creamos el pdf:
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )

            return response
        except:
            pass
        
        return HttpResponseRedirect(reverse_lazy('listaAutores'))  ##si llega a haber un error no me genera el pdf y se vuelve a la lista de autores

"""
## Para crear un nuevo punto:
def nuevoPunto(request):
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
    if os.path.isfile(autor.imagen.path):
        os.remove(autor.imagen.path)
    
    autor.delete()
    return redirect('listaAutores')
"""

######################################################################################################################



"""
from django.views.generic import View
from catalogo.models import ScoresReport

class reporteAutores(View):
	
    def get(self, request, *args, **kwargs):
    	# debemos obtener nuestro objeto classroom haciendo la consulta a la base de datos
        report = ScoresReport(Autor)
        return report.render_to_response()

## trabajando con reportes:
import os
from io import StringIO
import pyjasper #pyjasper

class reporteAutores():
    def compiling():
        input_file = 'C:\\Users\\gust\\OneDrive\\Documents\\detalleFinal\\ejemploDjango.jrxml'  
        jasper = pyjasper.JasperPy  #.JasperPy()
        jasper.compile(input_file)
        print("mi jasper es: ", jasper)

    def processing():
        input_file = 'C:\\Users\\gust\\OneDrive\\Documents\\detalleFinal\\ejemploDjango.jrxml'
        output = 'C:/Users/gust/Downloads' 
        jasper = pyjasper.JasperPy
        jasper.process(input_file, output=output, format_list=["pdf", "rtf"])
        print("Mi jasper proceso es: ",jasper)

    compiling
    processing
"""
# C:\Users\gust\OneDrive\Documents\detalleFinal\ejemploDjango.jasper   C:\Users\gust\OneDrive\Documents\detalleFinal

#'/examples/hello_world.jrxml'
#os.path.dirname(os.path.abspath(__file__)) + '/output/examples'

"""
from pyjasper import JasperGenerator
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring, fromstring

class reporteAutores(JasperGenerator):
    def __init__(self):
        super(self).__init__()
        self.reportname = 'C:/Users/gust/OneDrive/Documents/detalleFinal/ejemploDjango.jrxml' #'reports/Greeting.jrxml'
        self.xpath = '/autores/autores'
        self.root = ET.Element('autores')
    
    def generate_xml(self, tobegreeted):
        ET.SubElement(self.root, 'generator').text = '__revision__'

        for name in tobegreeted:
            xml_autores = ET.SubElement(self.root, 'autores')
            ET.SubElement(xml_autores, "autores_to").text = UNICODE(name)
            ET.SubElement(xml_autores, "autores_from").text = u"Max"
        return xmroot
    
    generator = reporteAutores()
    pdf = generator.generate(['nik', 'tobias', 'chris', 'daniel'])
    open('/tmp/greetingcard.pdf', 'w').write(pdf)    
"""