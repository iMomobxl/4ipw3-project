from django.shortcuts import render

def home(request):
    return render(request, "home.html", {} )

def article(request):
    return render(request, "article.html", {})

def recherche(request):
    return render(request, "recherche.html", {})

def test_font(request):
    return render(request, "test-font.html", {})
