from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('article/<int:pk>', views.article, name='article'),
    path('recherche/', views.recherche, name='recherche'),
    path('test-font/', views.test_font, name='test-font'),
    path('test-mysql/', views.test_mysql, name='test-mysql'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('login/', views.login, name='login'),
    path('user/', views.user, name='user'),
    path('style.css', views.style, name='style'),

]