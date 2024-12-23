from django.shortcuts import render
from .models import Category, Article
import requests
from pprint import pformat

def home(request):
    articles = Article.objects.filter(fk_category_art=146).order_by('-date_art')[:10]
    return render(request, "home.html", { 'articles': articles } )

def article(request):
    return render(request, "article.html", {})

def recherche(request):
    return render(request, "recherche.html", {})

def test_font(request):
    return render(request, "test-font.html", {})

def test_mysql(request):
    category = Category.objects.all()
    return render(request, "test-mysql.html", { 'category': category })

def sponsors(request):
    url = "http://playground.burotix.be/adv/banner_for_isfce.json"
    response = requests.get(url)
    data = response.json()
    formatted_data = pformat(data)
    print(formatted_data)
    banner_data = data.get('banner_4IPDW')
    return render(request, "sponsors.html", { 'data': banner_data, 'formatted_data': formatted_data})
