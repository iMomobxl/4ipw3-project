from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Article
import requests, csv, os
from django.conf import settings
from pprint import pformat
from .forms import LoginForm

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        uri_param = {
            'login': username,
            'passwd': password
        }
        uri_head = "http://playground.burotix.be/login/?"
        uri = f"{uri_head}{requests.compat.urlencode(uri_param)}"

        response = requests.post(uri)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if data.get('identified'):
                request.session['identified'] = data.get('identified')
                request.session['name'] = data.get('name')
                request.session['role'] = data.get('role')
                print(f"Identified: {request.session['identified']}")
                print(f"Name: {request.session['name']}")
                print(f"Role: {request.session['role']}")
                return redirect('user')
                # return render(request, 'user.html')
            else:
                messages.error(request,  f"Erreur dans le login/password")
        else:
            messages.error(request, f"Erreur: { response.status_code }")
    if request.session.get('identified'):
        return redirect('user')
    else:
        return render(request, 'login.html')


def user(request):
    if request.method == 'POST':
        request.session.clear()
        return redirect('home')
    if not request.session.get('identified', False):
        return redirect('login')
    return render(request, "user.html", {})