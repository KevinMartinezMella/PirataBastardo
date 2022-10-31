from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('busqueda', views.anime, name='busqueda'),
    path('episodios', views.verAnime, name='episodios'),
    path('verCapitulo', views.verCapitulo, name='verCap')
]