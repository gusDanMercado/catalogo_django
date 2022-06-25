from unicodedata import name
from django.urls import path
from catalogo import views

urlpatterns = [
    path('', views.index, name='index'),  ##para la pagina principal (Home)

    #path('generos', views.listaGeneros, name='listaGeneros'),  ##para la pagina de generos
    path('generos', views.listaGeneros.as_view(), name='listaGeneros'),  ##usando la clase ListView
    path('generos/detalle/<pk>', views.detalleGenero.as_view(), name='detalleGenero'),
    path('generos/nuevo', views.nuevoGenero, name='nuevoGenero'),  ##para realizar el formulario de carga de genero
    path('generos/actualizar/<pk>', views.actualizarGenero, name="actualizarGenero"),
    path('generos/eliminar/<pk>', views.eliminarGenero, name="eliminarGenero"),
    
    path('idiomas', views.listaIdiomas.as_view(), name='listaIdiomas'),
    path('idiomas/detalle/<pk>', views.detalleIdioma.as_view(), name='detalleIdioma'),
    path('idiomas/nuevo', views.nuevoIdioma, name='nuevoIdioma'),
    path('idiomas/actualizar/<pk>', views.actualizarIdioma, name='actualizarIdioma'),
    path('idiomas/eliminar/<pk>', views.elimanarIdioma, name='elimanarIdioma'),

    path('autores', views.listaAutores.as_view(), name='listaAutores'),
    path('autores/detalle/<pk>', views.detalleAutor.as_view(), name='detalleAutor'),
    path('autores/nuevo', views.nuevoAutor, name='nuevoAutor'),
    path('autores/actualizar/<pk>', views.actualizarAutor, name='actualizarAutor'),
    path('autores/eliminar/<pk>', views.eliminarAutor, name='eliminarAutor'),

    path('libros', views.listaLibros.as_view(), name='listaLibros'),
    path('libros/detalle/<pk>', views.detalleLibro.as_view(), name='detalleLibro'),
    path('libros/nuevo', views.nuevoLibro, name='nuevoLibro'),
    path('libros/actualizar/<pk>', views.actualizarLibro, name='actualizarLibro'),
    path('libros/eliminar/<pk>', views.eliminarLibro, name='eliminarLibro'),

    path('ejemplares', views.listaEjemplares.as_view(), name='listaEjemplares'),
    path('ejemplares/detalle/<pk>', views.detalleEjemplar.as_view(), name='detalleEjemplar'),
    path('ejemplares/nuevo', views.nuevoEjemplar, name='nuevoEjemplar'),
    path('ejemplares/actualizar/<pk>', views.actualizarEjemplar, name='actualizarEjemplar'),
    path('ejemplares/eliminar/<pk>', views.eliminarEjemplar, name='eliminarEjemplar'),

    path('graficos', views.chartData, name='graficos'),
    path('map', views.POIsMapView.as_view(), name='mapa'),
    
    ##path('puntos/lat/long', views.listaPuntos.as_view(),name='showroute'),
    #path('puntos', views.listaPuntos.as_view(), name='showmap'),
    #path('puntos/<str:lat>/<str:long>', views.listaPuntos_2.as_view(), name='showroute'),
    
    #path('idiomas', views.listaIdiomas.as_view(), name='listaIdiomas'), ##para la pagina de idiomas   
    #(lo hacemos asi porque usamos la clase ListView para manejar idiomas en views.py)
    
    #path('autores', views.listaAutores, name='listaAutores'), ##para la pagina de los autores
    #path('autores', views.listaAutores.as_view(), name='listaAutores'), ##para la pagina de los autores
    #path('autores/detalle/<pk>', views.detalleAutor.as_view(), name='detalleAutor'),
    #path('autores/actualizar/<pk>', views.actualizarAutor, name='actualizarAutor'),
    #path('autores/nuevo', views.nuevoAutor, name='nuevoAutor'),

    #path('libros', views.listaLibros, name='listaLibros'), ##para la pagina de los libros
    #path('libro/<pk>', views.detalleLibro.as_view(), name="detalleLibro"),
]