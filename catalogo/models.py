from audioop import reverse
from cgitb import text
from distutils.command.upload import upload
from email.mime import image
from email.policy import default
from faulthandler import disable
import uuid
from django.db import models

import os

# Create your models here.

#aqui tengo el modelo de todas las tablas que quiero tener en mi base de datos:

from django.core.validators import RegexValidator

class Autor(models.Model):
    apenom = models.CharField("Apellido y Nombre", max_length=50)  #"Apellido y Nombre" --> es lo que aparece como titulo de la columna cuando se muestra
    fechaNac = models.DateField("Fecha de Nacimiento", null=True)  #,null=True, blank=True
    fechaDeceso = models.DateField("Fecha de Deceso", null=True, blank=True)
    ##null=True --> da la opcion de que no se ingrese ninguna fecha (va a poner null)
    ##blank=True --> permite que este campo se quede en blanco para tus formularios
    imagen = models.ImageField(upload_to='autores', null=True, default='img/noposee_foto.png') #, blank=True

    def __str__(self):
        return '%s'%(self.apenom)  #esta clase me va a retornar el apellido y el nombre
    
    ##devuelve una URL para presentar registros individuales del modelo en el sitio web (este metodo añade automaticamente el boton "Ver en el Sitio")
    def get_absolute_url(self):
        return reverse('autorInfo', args=[str(self.apenom)])

    class Meta:
        ordering = ["apenom"] 

class Genero(models.Model):
    nombre = models.CharField(max_length=60, help_text="Ingrese el nombre del nuevo Genero (por ejemplo. Programacion, BD, SO, etc.)")

    #nombreRegex = RegexValidator('\d{3}-\d{2}-\d{5}-\d{2}-\d')
    #nombre = models.CharField(max_length=17, validators=[nombreRegex] ,help_text='Ingrese 13 digitos de la forma: XXX-XX-XXXXX-XX-X, para mas ayuda ingresar a <a href="https://www.isbn-international.org/es/content/%C2%BFqu%C3%A9-es-un-isbn" target="_blanck">Ayuda sobre el numero ISBN</a>')

    def __str__(self):
        return '%s '%(self.nombre)

    class Meta:
        ordering = ["nombre"]    

class Idioma(models.Model):
    nombre = models.CharField(max_length=25, help_text="Ingrese el nuevo Idioma (por ejemplo. Ingles, Español, etc.)")

    def __str__(self):
        return '%s'%(self.nombre)

##Notas: para este problema el libro va a tener un solo autor

class Libro(models.Model):
    titulo = models.CharField(max_length=200) #un nombre que no va a tener mas de 25 letras
    
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, help_text="Ingrese el autor (es uno solo)")
    ##ForeignKey --> es para indicar que es una relacion de uno a muchos (un libro tiene un solo autor y un autor puede tener muchos libros)
    ##el primer parametro que es Autor --> es modelo relacionado
    ##on_delete=models.SET_NULL --> pondra en null este campo si el registro o mejor dicho el autor
    ##es eliminado de la tabla Autor
    ##null=True --> permite almacenar automaticamente en la base de datos null si no se selecciono ningun autor para el libro

    resumen = models.TextField(max_length=1000, help_text="Ingrese el resumen del libro...")
    #ISBN = models.CharField(max_length=13, help_text='Ingrese 13 caracteres, para mas ayuda ingresar a <a href="https://www.isbn-international.org/es/content/%C2%BFqu%C3%A9-es-un-isbn" target="_blanck">Ayuda sobre el numero ISBN</a>')


    ##utilizando expresiones regulares:  (esto lo voy a realizar en Ejemplar ya que cada ejemplar del libro va a tener un ISBN unico)
    #isbnRegex = RegexValidator('\d{3}-\d{2}-\d{5}-\d{2}-\d')
    #ISBN = models.CharField(max_length=17, validators=[isbnRegex] ,help_text='Ingrese 13 digitos de la forma: xxx-xx-xxxxx-xx-x, para mas ayuda ingresar a <a href="https://www.isbn-international.org/es/content/%C2%BFqu%C3%A9-es-un-isbn" target="_blanck">Ayuda sobre el numero ISBN</a>')

    genero = models.ManyToManyField(Genero, help_text="Seleccione un genero(o varios) para este libro...")  #, null=True   
    ##ManyToManyField --> es para indicar que va a ser una relacion de muchos a muchos (un genero puede tener muchos libro y un libro puede tener varios generos)
    #on_delete=models.SET_NULL --> pondra en null este campo si el genero es borrado de su tabla
    #null=True --> da la opcion de que no se ingrese ningun genero (va a poner null)

    idioma = models.ForeignKey(Idioma, on_delete=models.SET_NULL, null=True) #aqui no hace falta el el vector de idioma ya que django lo hace automaticamente
    
    imagen= models.ImageField(upload_to='portadas', null=True, default='img/noposee_portada.png') ##  
    ##upload_to='img' --> me indica que la imagen se va a guardar en la carpeta img, tambien me crea esta carpeta

    def __str__(self):
        return '%s'%(self.titulo)  #, %s, %s, %s   , self.genero.nombre, self.autor, self.ISBN   , %s  , self.resumen
    
    def get_absolute_url(self):
        return reverse("LibroInfo", args=[str(self.id)])

    ##como Django no permite visualizar relaciones muchos a muchos, agregamos:
    def muestra_genero(self):
        return ', '.join([genero.nombre for genero in self.genero.all()[:3]])
    
    muestra_genero.short_description = 'Genero/s' 

    ##para mostrar nuestros registros ordenados al consultar el modelo utilizamos:
    class Meta:
        ordering = ["titulo"]  #ordering = ["fechaDevolucion"]

        def __str__(self):
            return '%s'%(self.titulo)  #, %s, %s, %s   , self.genero.nombre, self.autor, self.ISBN   , %s  , self.resumen

class Ejemplar(models.Model):
    uniqueId = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unico para este libro particular en toda la biblioteca...")
    ##donde:
    ##UUIDField --> se usa para establecer el campo id como un PK para este modelo.
    ##default=uuid.uuid4 --> uuid es un modulo que proporciona objetos inmutables, este objeto llama a la funcion:
    ##uuid4 para crear una UUID aleatoria, es decir, creamos una identificacion o ID unico 
    ##esta clase: uuid tambien posee otras funciones como ser: uuid1 (puede comprometer la privacidad), uuid3, uuid4, uuid5 

    ##utilizando expresiones regulares:  (esto lo voy a realizar en Ejemplar ya que cada ejemplar del libro va a tener un ISBN unico)
    isbnRegex = RegexValidator('\d{3}-\d{2}-\d{5}-\d{2}-\d')
    ISBN = models.CharField(unique=True, max_length=17, validators=[isbnRegex] ,help_text='Ingrese 13 digitos de la forma: XXX-XX-XXXXX-XX-X, para mas ayuda ingresar a <a href="https://www.isbn-international.org/es/content/%C2%BFqu%C3%A9-es-un-isbn" target="_blanck">Ayuda sobre el numero ISBN</a>')   
    # , blank=True
    
    fechaDevolucion = models.DateField("Fecha de Devolución" , null=True, blank=True)

    ESTADO_PRESTAMO = (
        ('m', 'en Mantenimiento'),
        ('p', 'Prestado'),
        ('d', 'Disponible'),
        ('r', 'Reservado')
    )  #defino una lista de posibles estados en el que puede estar un libro
    estado = models.CharField(max_length=1, default='d', help_text="Ingrese Disponibilidad del ejemplar...", choices=ESTADO_PRESTAMO)
    # default='d' --> por defecto si no ingresamos ningun valor va a tomar el valor de d(Disponible)
    # choises --> me brinda las multiples opciones de los estados de prestamo 

    libro = models.ForeignKey(Libro, on_delete=models.SET_NULL, null=True)
    #aqui decimos que un libro va a tener muchos ejemplares y un ejemplar va a pertenecer a un unico libro

    def __str__(self):
        #return '%s, %s, %s'%(self.uniqueId, self.fechaDevolucion, self.estado) #   self.get_estado_display()
        return '%s, %s, %s'%(self.uniqueId, self.fechaDevolucion, self.estado) #   self.get_estado_display()

    ##para mostrar nuestros registros ordenados al consultar el modelo utilizamos:
    class Meta:
        ordering = ["libro"]  #ordering = ["fechaDevolucion"]

        def __str__(self):
            return '%s (%s)'%(self.id, self.libro.titulo)

##otra relacion que puede haber es: OneToOneField --> es para indicar la relacion de uno a uno

## Definimos un modelo para mostrar el Mapa:

class POI(models.Model):
    nombre = models.CharField(max_length=255)
    lng = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '%s'%(self.nombre)


### extendemos el modelo User que viene por defecto en Django para agregarle algunos campos

from django.contrib.auth.models import User

class Ubicacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text="Ingrese el usuario")
    poi = models.ForeignKey(POI, on_delete=models.SET_NULL, null=True, help_text="Ingrese direccion" )

    def __str__(self):
        return '%s'%(self.usuario.username, self.poi.nombre)
