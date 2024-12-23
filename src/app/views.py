from django.shortcuts import render
from .models import Category

def home(request):
    return render(request, "home.html", {} )

def article(request):
    return render(request, "article.html", {})

def recherche(request):
    return render(request, "recherche.html", {})

def test_font(request):
    return render(request, "test-font.html", {})

def test_mysql(request):
    category = Category.objects.all()
    return render(request, "test-mysql.html", { 'category': category })
