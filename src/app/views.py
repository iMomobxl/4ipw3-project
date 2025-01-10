from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import DatabaseError, connection
from django.db.models import Min, Max
from django.conf import settings
from .models import Category, Article, Static
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
        favoris = json.loads(favoris)
        user_name = request.session.get('name')
        print(favoris)
        is_favorite = any(item['id_art'] == str(id) and item['name'] == user_name for item in favoris)
        print(is_favorite)
        # is_favorite = str(id) in favoris
    except DatabaseError as error:
        article = []
        is_favorite = False
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
        max_nbr_article = request.POST.get('max_nbr_article', 'off')
        if max_nbr_article == 'on':
            nbr_article = None
        else:
            nbr_article = request.POST.get('nbr_article', None)

        tri_article = request.POST.get('tri_article', '-date_art')

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
        try:
            articles = Article.objects.filter(**param_search).order_by(tri_article)[:nbr_article]
            if articles.exists():
                messages.success(request, "Nous avons obtenu un resultat pour votre recherche.")
                return render(request, "recherche.html", { 'articles': articles })
            else:

                context = get_recherche_context()
                context.update(param_search)
                print(context)
                messages.warning(request, "Pas de résultat pour votre recherche, recommencé...")
                return render(request, 'recherche.html', context)
        except DatabaseError as error:
            messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
            print(f"Database error: {error}")
            return redirect('recherche')
    else:
        context = get_recherche_context()
        return render(request, "recherche.html", context)

def test_font(request):
    return render(request, "test-font.html", {})

def test_mysql(request):
    tables_info = {}
    nbr_ligne = {}
    try:
        table_names = ['t_article', 't_category', 't_static']
        for table in table_names:
            with connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {table}")
                columns = cursor.fetchall()
                tables_info[table] = columns
    except DatabaseError as error:
        tables_info = {}
        messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
        print(f"Database error: {error}")
    print(nbr_ligne)
    return render(request, "test-mysql.html", { 'tables_info': tables_info })

def sponsors(request):
    url = "http://playground.burotix.be/adv/banner_for_isfce.json"
    response = requests.get(url)
    data = response.json()
    formatted_data = pformat(data)

    # Ajout test plusieurs bannieres - desactiver les commentaire pour tester
    #
    # test = {'banner_4IPDW': {'background_image': 'https://www.burotix.be/images/light-bulb-1002783_480.jpg',
    #                                   'color': '#0dd3d1',
    #                                   'image': 'https://www.burotix.be/images/keyboard-824317_120.jpg',
    #                                   'link': 'https://www.burotix.be/',
    #                                   'text': 'Entrepreneur... ?\n' '\t\t\tBUROTIX(), sise à Walhain dans le Brabant ' "Wallon, optimise l'emploi de vos\n" '\t\t\ttableurs, bases de données, sites web, ' 'dossiers administratifs, etc.'},
    #         'banner_3IPDW': {'background_image': 'https://www.burotix.be/images/light-bulb-1002783_480.jpg',
    #                                   'color': '#0dd3d1',
    #                                   'image': 'https://www.burotix.be/images/keyboard-824317_120.jpg',
    #                                   'link': 'https://www.burotix.be/',
    #                                   'text': 'Indépendant... ?\n' '\t\t\tBUROTIX(), sise à Walhain dans le Brabant ' "Wallon, optimise l'emploi de vos\n" '\t\t\ttableurs, bases de données, sites web, ' 'dossiers administratifs, etc.'},
    #         'banner_2IPDW': {'background_image': 'https://www.burotix.be/images/light-bulb-1002783_480.jpg',
    #                          'color': '#0dd3d1',
    #                          'image': 'https://www.burotix.be/images/keyboard-824317_120.jpg',
    #                          'link': 'https://www.burotix.be/',
    #                          'text': 'Artisan... ?\n' '\t\t\tBUROTIX(), sise à Walhain dans le Brabant ' "Wallon, optimise l'emploi de vos\n" '\t\t\ttableurs, bases de données, sites web, ' 'dossiers administratifs, etc.'}
    # }
    # return render(request, "sponsors.html", { 'data': test, 'formatted_data': pformat(test) })

    return render(request, "sponsors.html", { 'data': data, 'formatted_data': formatted_data })


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
                messages.warning(request,  "Erreur dans le login/password, recommencez...")
        else:
            messages.warning(request, f"Code Erreur: { response.status_code }")
    if request.session.get('identified'):
        messages.warning(request, "Vous êtes deja logé, je vous envoie sur votre page utilisateur (user) ")
        return redirect('user')
    else:
        return render(request, 'login.html')

def user(request):
    if request.method == 'POST':
        if 'about' in request.POST:
            about = Static.objects.get(id_sta=1)
            about.content_sta = request.POST.get('about', None)
            about.save()
            messages.success(request, "Le contenu de la page About á été mis á jour.")
            return redirect('about')
        elif 'font_color' in request.POST or 'border_style' in request.POST:
            font_color = request.POST.get('font_color', 'none')
            border_style = request.POST.get('border_style', 'black')
            home_category = request.POST.get('home_category', 146)
            request.session['font_color'] = font_color
            request.session['border_style'] = border_style
            request.session['home_category'] = home_category
            messages.success(request, "Vos préférences ont été mises à jour.")
        else:
            request.session.clear()
            messages.success(request, "Vous venez de vous logout, á bientôt.")
            return redirect('home')
    if not request.session.get('identified', False):
        messages.warning(request, f"Vous devez etre logé pour acceder à cette page")
        return redirect('login')
    try:
        about = get_object_or_404(Static,id_sta=1)
        category = Category.objects.all()
        print(about)
    except DatabaseError as error:
        category = []
        about = []
        messages.warning(request,"Erreur de connection á la DB. Revenez plus tard.")
        print(f"Database error: {error}")
    return render(request, "user.html", { 'category': category, 'about': about })

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
        messages.warning(request, "Vous devez être logé pour accéder à cette page")
        return redirect('login')
    else:
        user_name = request.session.get('name')
        favoris = request.COOKIES.get('favoris', '[]')
        favoris = json.loads(favoris)

        favoris = [
            item['id_art'] for item in favoris if item['name'] == user_name
        ]
        try:
            articles = Article.objects.filter(id_art__in=favoris)
        except DatabaseError as error:
            articles = []
            messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
            print(f"Database error: {error}")
        return render(request, 'favoris.html', { 'articles': articles })

def add_favoris(request, id):
    if not request.session.get('identified', False):
        messages.warning(request, "Vous n'avez pas acces á cette page.")
        return render(request, '404.html', status=404)
    else:
        try:
            if not Article.objects.filter(id_art=id).exists():
                messages.warning(request, f"L'article avec l'ID {id} n'existe pas.")
                return redirect('home')
        except DatabaseError as error:
            messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
            print(f"Database error: {error}")
            return redirect('home')
        user_name = request.session.get('name')
        favoris = request.COOKIES.get('favoris', '[]')
        favoris = json.loads(favoris)

        current_favoris = {'name': user_name, 'id_art': str(id)}

        if current_favoris not in favoris:
            favoris.append(current_favoris)
        else:
            messages.warning(request, "Cette articles est déjá present dans vos favoris.")
            return redirect('favoris')
        favoris = json.dumps(favoris)
        response = redirect('article', id=id)
        response.set_cookie('favoris', favoris)
        messages.success(request, "Cette articles a été rajouté á vos favoris.")
        return response

def del_favoris(request, id):
    if not request.session.get('identified', False):
        messages.warning(request, "Vous n'avez pas accés á cette page.")
        return render(request, '404.html', status=404)
    else:
        user_name = request.session.get('name')
        favoris = request.COOKIES.get('favoris', '[]')
        favoris = json.loads(favoris)

        current_favoris = {'name': user_name, 'id_art': str(id)}
        if current_favoris in favoris:
            favoris.remove(current_favoris)
        # if str(id) in favoris:
        #     favoris.remove(str(id))
        else:
            messages.warning(request, "Cette article ne se trouve pas dans vos favoris.")
            return redirect('favoris')
        favoris = json.dumps(favoris)
        response = redirect('article', id=id)
        response.set_cookie('favoris', favoris)
        messages.success(request, "Cette article a été supprimé de vos favoris.")
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

def about(request):
    try:
        content = get_object_or_404(Static, url_sta='about')
    except DatabaseError as error:
        content = []
        messages.warning(request, "Erreur de connection á la DB. Revenez plus tard.")
        print(f"Database error: {error}")
    return render(request, 'about.html', { 'content': content })

# cherche le min/max du champ readtime pour set le min et max dans la page recherche
# ainsi que les categories
def get_recherche_context():
    try:
        category = Category.objects.all()
        max_readtime = Article.objects.all().aggregate(Max('readtime_art'))['readtime_art__max']
        min_readtime = Article.objects.all().aggregate(Min('readtime_art'))['readtime_art__min']
    except DatabaseError as error:
        category = []
        max_readtime = 1
        min_readtime = 1
        print(f"Database error: {error}")
    return { 'category': category, 'max_readtime': max_readtime, 'min_readtime': min_readtime }

