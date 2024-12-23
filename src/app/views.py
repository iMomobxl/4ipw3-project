from django.shortcuts import render
from .models import Category, Article

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
