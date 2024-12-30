from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import DatabaseError
from django.db.models import Min, Max
from django.conf import settings
from .models import Category, Article
import requests, csv, os, json
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
    category_art = request.session.get('home_category', "146") # 146 = On n'est pas des pigeons
    try:
        articles = Article.objects.filter(fk_category_art=category_art).order_by('-date_art')[:9]
    except DatabaseError as error:
        articles = []
        messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
        print(f"Database error: {error}")
    # menu = display_menu_csv()
    # print(menu)
    return render(request, "home.html", { 'articles': articles })

def article(request, id):
    try:
        article = get_object_or_404(Article,id_art=id)
        favoris = request.COOKIES.get('favoris', '[]')
        favoris_ids = json.loads(favoris)
        is_favorite = str(id) in favoris_ids
    except DatabaseError as error:
        article = []
        messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
        print(f"Database error: {error}")
    return render(request, 'article.html', { 'article': article, 'is_favorite': is_favorite })

def recherche(request):
    if request.method == 'POST':
        mot_title = request.POST.get('mot_title', None)
        mot_content = request.POST.get('mot_content', None)
        mot_hook = request.POST.get('mot_hook', None)
        date = request.POST.get('date', None)
        category = request.POST.get('category', None)
        readtime = request.POST.get('readtime', 1)
        nbr_article = request.POST.get('nbr_article', None)
        tri_article = request.POST.get('tri_article', None)

        param_search = { 'readtime_art': readtime }

        if category != '0' and category != None:
            param_search['fk_category_art'] = category
        if date:
            param_search['date_art'] = date
        if mot_title:
            param_search['title_art__icontains'] = mot_title
        if mot_hook:
            param_search['hook_art__icontains'] = mot_hook
        if mot_content:
            param_search['content_art__icontains'] = mot_content
        if nbr_article:
            nbr_article = int(nbr_article)
        print(param_search)
        try:
            articles = Article.objects.filter(**param_search).order_by('-date_art')[:nbr_article]
            if articles.exists():
                messages.success(request, "Résultat de la recherche ok")
                return render(request, "recherche.html", { 'articles': articles })
            else:
                messages.warning(request, "Pas de résultat pour votre recherche, recommencé...")
                return redirect('recherche')
        except DatabaseError as error:
            messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
            print(f"Database error: {error}")
            return redirect('recherche')
    else:
        try:
            category = Category.objects.all()
            max_readtime = Article.objects.all().aggregate(Max('readtime_art'))
            min_readtime = Article.objects.all().aggregate(Min('readtime_art'))
            max = max_readtime['readtime_art__max']
            min = min_readtime['readtime_art__min']
        except DatabaseError as error:
            category = []
            messages.warning(request,"Erreur de connection á la DB. Revenez plus tard.")
            print(f"Database error: {error}")
        return render(request, "recherche.html", {
            'category': category,
            'max_readtime': max,
            'min_readtime': min
        })

def test_font(request):
    return render(request, "test-font.html", {})

def test_mysql(request):
    try:
        category = Category.objects.all()
    except DatabaseError as error:
        category = []
        messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
        print(f"Database error: {error}")
    return render(request, "test-mysql.html", { 'category': category })

def sponsors(request):
    url = "http://playground.burotix.be/adv/banner_for_isfce.json"
    response = requests.get(url)
    data = response.json()
    formatted_data = pformat(data)
    banner_data = data.get('banner_4IPDW')
    return render(request, "sponsors.html", { 'data': banner_data, 'formatted_data': formatted_data })

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
        if 'font_color' in request.POST or 'border_style' in request.POST:
            font_color = request.POST.get('font_color', 'none')
            border_style = request.POST.get('border_style', 'black')
            home_category = request.POST.get('home_category', 146)
            request.session['font_color'] = font_color
            request.session['border_style'] = border_style
            request.session['home_category'] = home_category
            messages.success(request, "Vos préférences ont été mises à jour.")
        else:
            request.session.clear()
            messages.success(request, f"Vous n'etes plus logé, BYEBYE")
            return redirect('home')
    if not request.session.get('identified', False):
        messages.warning(request, f"Vous devez etre logé pour acceder à cette page")
        return redirect('login')
    try:
        category = Category.objects.all()
    except DatabaseError as error:
        category = []
        messages.warning(request,"Erreur de connection á la DB. Revenez plus tard.")
        print(f"Database error: {error}")
    return render(request, "user.html", { 'category': category })

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

def favoris(request):
    if not request.session.get('identified', False):
        messages.warning(request, f"Vous devez etre logé pour acceder à cette page")
        return redirect('login')
    else:
        favoris = request.COOKIES.get('favoris', '[]')
        favoris_ids = json.loads(favoris)
        try:
            articles = Article.objects.filter(id_art__in=favoris_ids)
        except DatabaseError as error:
            articles = []
            messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
            print(f"Database error: {error}")
        return render(request, 'favoris.html', { 'articles': articles })

def add_favoris(request, id):
    if not request.session.get('identified', False):
        messages.warning(request, f"Vous n'avez pas acces á cette page.")
        return render(request, '404.html', status=404)
    else:
        favoris = request.COOKIES.get('favoris', '[]')
        favoris = json.loads(favoris)
        if str(id) not in favoris:
            favoris.append(str(id))
        else:
            messages.warning(request, f"Cette articles est déjá present dans vos favoris.")
            return redirect('favoris')
        favoris = json.dumps(favoris)
        response = redirect('article', id=id)
        response.set_cookie('favoris', favoris)
        messages.success(request, f"Cette articles a été rajouté dans vos favoris.")
        return response

def del_favoris(request, id):
    if not request.session.get('identified', False):
        messages.warning(request, f"Vous n'avez pas acces á cette page.")
        return render(request, '404.html', status=404)
    else:
        favoris = request.COOKIES.get('favoris', '[]')
        favoris = json.loads(favoris)
        if str(id) in favoris:
            favoris.remove(str(id))
        else:
            messages.warning(request, f"Cette articles ne se trouve pas dans vos favoris pour pouvoir le supprimer.")
            return redirect('favoris')
        favoris = json.dumps(favoris)
        response = redirect('article', id=id)
        response.set_cookie('favoris', favoris)
        messages.success(request, f"Cette articles a été supprimé de vos favoris.")
        return response

def date_list(request):
    try:
        dates = Article.objects.values_list('date_art', flat=True).distinct().order_by('-date_art')
    except DatabaseError as error:
        dates = []
        messages.warning(request,"Erreur de connection á la DB. Revenez plus tard.")
        print(f"Database error: {error}")
    return render(request, 'date_list.html', { 'dates' : dates })

def date_list_with_date(request,date):
    try:
        articles = Article.objects.filter(date_art=date).order_by('-date_art')
    except DatabaseError as error:
        articles = []
        messages.error(request, "Erreur de connection á la DB. Revenez plus tard.")
        print(f"Database error: {error}")
    return render(request, 'date_list.html', { 'articles': articles, 'date_select': date })
