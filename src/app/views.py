from django.shortcuts import render, get_object_or_404
from .models import Category, Article
import requests, csv, os
from django.conf import settings
from pprint import pformat

# def display_menu_csv():
#     menu_items = []
#     csv_path = os.path.join(settings.BASE_DIR, 'asset', 'menu.csv')
#     with open(csv_path, mode='r') as file:
#         csv_reader = csv.DictReader(file, delimiter='|')
#         for row in csv_reader:
#             menu_items.append({'id': row['id'], 'name': row['name']})
#     return menu_items

def home(request):
    articles = Article.objects.filter(fk_category_art=146).order_by('-date_art')[:10]
    # menu = display_menu_csv()
    # print(menu)
    return render(request, "home.html", { 'articles': articles })

def article(request):
    article_id = request.GET.get('id')
    article = get_object_or_404(Article, id_art=article_id)
    return render(request, 'article.html', { 'article': article })

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
    banner_data = data.get('banner_4IPDW')
    return render(request, "sponsors.html", { 'data': banner_data, 'formatted_data': formatted_data})

def login(request):
    return render(request, "login.html", {})

def user(request):
    return render(request, "user.html", {})