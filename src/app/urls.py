from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('article/<int:id>', views.article, name='article'),
    path('recherche/', views.recherche, name='recherche'),
    path('test-font/', views.test_font, name='test-font'),
    path('test-mysql/', views.test_mysql, name='test-mysql'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('login/', views.login, name='login'),
    path('user/', views.user, name='user'),
    path('style.css', views.style, name='style'),
    path('favoris/', views.favoris, name='favoris'),
    path('favoris/add/<int:id>', views.add_favoris, name='add_favoris'),
    path('favoris/del/<int:id>', views.del_favoris, name='del_favoris'),
    path('date_list/', views.date_list, name='date_list'),
    path('date_list/<str:date>/', views.date_list_with_date, name='date_list_with_date'),
    path('about/', views.about, name='about'),
]