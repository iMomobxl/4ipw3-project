from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from .models import Category, Article
import requests, csv, os
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
    articles = Article.objects.filter(fk_category_art=146).order_by('-date_art')[:9]
    # menu = display_menu_csv()
    # print(menu)
    return render(request, "home.html", { 'articles': articles })

def article(request,pk):
    article_id = Article.objects.get(id_art=pk)
    return render(request, 'article.html', { 'article': article_id })

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
                messages.success(request, f"Vous etes logé en tand que { request.session['role'] }, Bienvenue { request.session['name'] }")
                return redirect('user')
            else:
                messages.warning(request,  f"Erreur dans le login/password")
        else:
            messages.warning(request, f"Code Erreur: { response.status_code }")
    if request.session.get('identified'):
        messages.warning(request, f"Vous etes deja logé, je vous envoie sur votre page utilisateur (user) ")
        return redirect('user')
    else:
        return render(request, 'login.html')


def user(request):
    if request.method == 'POST':
        print("Request Method:", request.method)
        print("GET Parameters:", request.GET)
        print("POST Parameters:", request.POST)
        print("COOKIES:", request.COOKIES)
        print("Session Data:", dict(request.session.items()))
        if 'font_color' in request.POST or 'border_style' in request.POST:
            font_color = request.POST.get('font_color', 'none')
            border_style = request.POST.get('border_style', 'black')
            request.session['font_color'] = font_color
            request.session['border_style'] = border_style
            messages.success(request, "Vos préférences ont été mises à jour.")
        else:
            request.session.clear()
            messages.success(request, f"Vous n'etes plus logé, BYEBYE")
            return redirect('home')
    if not request.session.get('identified', False):
        messages.warning(request, f"Vous devez etre logé pour acceder à cette page")
        return redirect('login')
    return render(request, "user.html", {})



def style(request):
    font_color = request.session.get('font_color', 'black')
    border_style = request.session.get('border_style', 'none')

    border_width = '0px'
    if border_style == 'thin':
        border_width = '2px'
    elif border_style == 'thick':
        border_width = '4px'

    css_content = f"""
    body {{
        color: { font_color };
        border: { border_width } solid;
    }}
    """
    return HttpResponse(css_content, content_type='text/css')
