from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('home.html', views.home, name='home'),
    path('article.html', views.article, name='article'),
    path('recherche.html', views.recherche, name='recherche'),
    path('test-font.html', views.test_font, name='test-font'),
]