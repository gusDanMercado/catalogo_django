from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from catalogo.models import Autor, Genero, Idioma, Libro, Ejemplar, POI

class AutorAdmin(admin.ModelAdmin):
    list_display = ('apenom', 'fechaNac', 'imagen')   #son todas las columnas que va a mostrar en el sitio de administracion de Django
    list_filter = ('apenom', 'fechaNac')  #son los filtros que va a mostrar al lado derecho del sitio de administracion de Django

class GeneroAdmin(admin.ModelAdmin):
    pass
    
class IdiomaAdmin(admin.ModelAdmin):
    pass

class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'idioma', 'muestra_genero', 'imagen_Portada')  #, 'ISBN'
    list_filter = (('titulo',)) ##, 'ISBN'

    def imagen_Portada(self, obj):
        return format_html('<img src={} width=200 heigth=100 />', obj.imagen.url)


class EjemplarAdmin(admin.ModelAdmin):
    list_display = ('libro', 'estado', 'fechaDevolucion')   #son todas las columnas que va a mostrar en el sitio de administracion de Django
    #list_display = ('libro', 'ISBN', 'estado', 'fechaDevolucion')
    list_filter = (('ISBN', 'estado','fechaDevolucion'))  #son los filtros que va a mostrar al lado derecho del sitio de administracion de Django


class POIAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'lng', 'lat')

admin.site.register(Autor, AutorAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Idioma, IdiomaAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Ejemplar, EjemplarAdmin)
admin.site.register(POI, POIAdmin)