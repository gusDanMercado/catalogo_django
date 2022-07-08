from asyncio.windows_events import NULL
from email.headerregistry import Group
from enum import auto
from logging import raiseExceptions
from multiprocessing import context
from pyexpat import model
from select import select
from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
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
            raise Http404("Ooops! El Libro no existe")
        
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

    #print("La direccion de la imagen es: ",libro.imagen.path)

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
    paginate_by = 5
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

## Para actualizar un ejemplar: 
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


####################################### USUARIOS #####################################################################
## Vamos a utilizar el modelo User que ya viene por defecto en Django y a es modelo le vamos a agregar campos que me 
## hacen falta

from django.contrib.auth.models import User, Group
from catalogo.forms import UsuarioForm, UsuarioForm2

## Para ver todos los usuarios:
class listaUsuarios(generic.ListView):    
    model = User #.objects.filter(groups__name='usuarios_catalogo')   ##me tira error ya que tengo que definir el queryset

    ordering = ['username']

    def get_queryset(self):
        return super().get_queryset().filter(groups__name='usuarios_catalogo')
    
    context_object_name = 'usuarios'
    paginate_by = 5
    template_name = 'usuario/usuarios.html'

## Para ver un usuario:
class detalleUsuario(generic.DetailView):
    model = User
    #print("estoy aqui 1232132132123", model.objects.values_list())
    template_name = 'usuario/detalleUsuario.html'

    def user_detalle_view(request, pk):
        try:
            usuario = User.objects.get(pk = pk)
        except User.DoesNotExist:
            raise Http404("Ooops! El Usuario no existe")
        
        context = {
            'usuario' : usuario
        }

        return render(request, 'detalleUsuario.html', context)

## Para crear un nuevo Usuario:
def crearUsuario(request):
    if request.method == "POST":
        formulario = UsuarioForm2(request.POST)  #crear
        print("El formulario es: ", formulario)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
     
            usuario.username = formulario.cleaned_data['username']
            usuario.first_name = formulario.cleaned_data['first_name']
            usuario.last_name = formulario.cleaned_data['last_name']
            usuario.email = formulario.cleaned_data['email']

            usuario.save()

            ##agregamos este usuario a un grupo: (esto se hace asi porque estos usuarios solo van a tener determinados permisos, el cual se los va a dar el admin)
            group = Group.objects.get(name='usuarios_catalogo')
            usuario.groups.add(group)

            return redirect('listaUsuarios')
    else:
        formulario = UsuarioForm2()  
    
    return render(request, 'usuario/crearUsuario.html', { 'formulario' : formulario })

## Para actualizar un usuario: 
def actualizarUsuario(request, pk):
    usuario = get_object_or_404(User, pk = pk)

    if request.method == "POST":
        formulario = UsuarioForm(request.POST, instance=usuario)  

        if formulario.is_valid():

            usuario.username = formulario.cleaned_data['username']
            usuario.first_name = formulario.cleaned_data['first_name']
            usuario.last_name = formulario.cleaned_data['last_name']
            usuario.email = formulario.cleaned_data['email']

            usuario.save()
            
            return redirect('listaUsuarios')
    else:
        formulario = UsuarioForm(instance=usuario) 
    
    return render(request, 'usuario/crearUsuario.html', { 'formulario' : formulario })

## Para eliminar un usuario especifico
def eliminarUsuario(request, pk):
    usuario = get_object_or_404(User, pk = pk)
    usuario.delete()
    return redirect('listaUsuarios')
######################################################################################################################


####################################### GRAFICOS #####################################################################
def chartData(request):
    chartLabel = "Prestamos"
    etiquetas = []
    #minimo = 10
    #maximo = 100
    datos = []

    libros = Libro.objects.all()

    for libro in libros:
        etiquetas.append(libro.titulo)
        #ejemplares = Ejemplar.objects.filter(libro__pk=libro.pk).count()  ##cantidad de ejemplares de cada libro
        ejemplares = Ejemplar.objects.filter(libro__pk=libro.pk).filter(estado__exact='d').count()  ##cantidad de ejemplares disponibles de cada libro
        datos.append(ejemplares)

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


####################################### REPORTES #####################################################################

####################################### AUTORES ######################################################################
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape

from reportlab.lib.pagesizes import A4
from datetime import date
from django.core import serializers

from reportlab.lib.utils import ImageReader

def AutorReport(request):
    today = date.today().strftime('%Y-%m-%d')
    buffer = io.BytesIO()
    report = canvas.Canvas(buffer, pagesize=A4)

    data = Autor.objects.all()  ## modelo Autor
    print("Los autores cargados son: ",data)

    report.setFont('Helvetica',15, leading=None)
    report.setFillColorRGB(0,0,0)  ##color
    report.drawString(260,800,'Catalogo de Autores')
    report.line(100,780,500,780)  #0,780,1000,780  100,780,500,780

    x1=20
    y1=750
    counter = 0

    object_list= serializers.serialize("python", data)
    #print("mi object_list es: ",object_list)
    #Esto nos muestra: #[{'model': 'catalogo.autor', 'pk': 11, 'fields': {'apenom': 'Jacob Kaplan Moss', 'fechaNac': datetime.date(1982, 7, 9), 'fechaDeceso': None, 'imagen': 'autores/autor2Django.jpg'}}, {'model': 'catalogo.autor', 'pk': 12, 'fields': {'apenom': 'Alan Bool', 'fechaNac': datetime.date(1958, 10, 15), 'fechaDeceso': datetime.date(1980, 1, 30), 'imagen': 'autores/George_Boole.jpg'}}, {'model': 'catalogo.autor', 'pk': 15, 'fields': {'apenom': 'Adrian Holovaty', 'fechaNac': datetime.date(1983, 2, 2), 'fechaDeceso': None, 'imagen': 'autores/fondo2.jpg'}}]
    ##es un diccionario para poder todos los datos que tiene el modelo Libro

    for object in object_list:
        counter= counter + 1

        for field_name, field_value in object['fields'].items():
            if counter==1:  ## primera fila (etiquetas)
                report.setFont("Times-Roman",12,leading=None)
                report.drawString(x1+100,y1,field_name) 
            else:  ## segunda fila en adelante (valores)
                report.setFont("Helvetica",11,leading=None)
                if field_name=='fechaNac' or field_name=='fechaDeceso':                        
                    if field_value!=None:
                        valor=str(field_value)
                    else:
                        valor='no posee'
                else:
                    valor=field_value   

                if field_name == 'imagen':
                    dirImg = 'E:/DesarrolloWeb2022/Django/Proyecto2/media/'+valor
                    img = ImageReader(dirImg)
                    report.drawImage(img, x1+100,y1, 30, 30)
                else:
                    report.drawString(x1+100,y1, valor)

            x1 = x1 + 100   ##columnas eje horizontal
        y1 = y1 - 40        ##filas eje vertical

        x1=20
        if counter == 1:   ## es para la primera fila (los valores)
            for field_name, field_value in object['fields'].items():
                report.setFont("Helvetica",11,leading=None)
                if field_name=='fechaNac' or field_name=='fechaDeceso':
                    if field_value!=None:
                        valor=str(field_value)
                    else:
                        valor='no posee'
                else:
                    valor=field_value   

                if field_name == 'imagen':
                    dirImg = 'E:/DesarrolloWeb2022/Django/Proyecto2/media/'+valor
                    img = ImageReader(dirImg)  

                    report.drawImage(img, x1+100,y1, 30, 30)
                else:
                    report.drawString(x1+100,y1, valor)   
                
                x1 = x1 + 100
            
            y1 = y1 - 40  ##filas eje vertical
            x1=20

    report.setTitle(f'Autores: Reporte del {today}')
    report.showPage()
    report.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="reporte.pdf")

######################################################################################################################

####################################### GENERICO #####################################################################

import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

class PDFreporte(View):

    def get(self, request, *args, **kwargs):

        try:
            template = get_template('reporteGeneral.html')

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
                'totalEje' : Ejemplar.objects.count(),
                'title4' : 'Lista de Usuarios',
                'usuarios' : User.objects.all().filter(groups__name='usuarios_catalogo').order_by('username'),
                'totalUsu' : User.objects.filter(groups__name='usuarios_catalogo').count()
            }

            html = template.render(context)

            response = HttpResponse() ##context_type = 'application/pdf'
            response['Content-Disposition'] = 'attachment; filename="reporteGeneral.pdf"'  ##   esta opcion hace que se me descarge el archivo

            ##creamos el pdf:
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )

            return response
        except:
            pass
        
        return HttpResponseRedirect(reverse_lazy('index'))  ##si llega a haber un error no me genera el pdf y se vuelve a la lista de autores

######################################################################################################################

######################################################################################################################