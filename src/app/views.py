from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import DatabaseError, connection
from django.db.models import Min, Max
from django.core.paginator import Paginator
from .models import Category, Article, Static
import requests, json
from pprint import pformat

def home(request):
    category_art = request.session.get('home_category', "146") # 146 = On n'est pas des pigeons
    try:
        articles = Article.objects.filter(fk_category_art=category_art).order_by('-date_art')[:9]
        favoris = request.COOKIES.get('favoris', '[]')
        favoris = json.loads(favoris)
        user_name = request.session.get('name')
        for article in articles:
            article.is_favorite = any(item['id_art'] == str(article.id_art) and item['name'] == user_name for item in favoris)
    except DatabaseError as error:
        articles = []
        request.session['message'] = "Erreur de connection á la DB. Revenez plus tard."
        request.session['message_status'] = "warning"
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
    except DatabaseError as error:
        article = []
        is_favorite = False
        request.session['message'] = "Erreur de connection á la DB. Revenez plus tard."
        request.session['message_status'] = "warning"
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
                request.session['message'] = "Nous avons obtenu un resultat pour votre recherche."
                request.session['message_status'] = "success"
                return render(request, "recherche.html", { 'articles': articles })
            else:

                context = get_recherche_context()
                context.update(param_search)
                request.session['message'] = "Pas de résultat pour votre recherche, recommencé..."
                request.session['message_status'] = "warning"
                return render(request, 'recherche.html', context)
        except DatabaseError as error:
            request.session['message'] = "Erreur de connection á la DB. Revenez plus tard."
            request.session['message_status'] = "warning"
            print(f"Database error: {error}")
            return redirect('recherche')
    else:
        context = get_recherche_context()
        return render(request, "recherche.html", context)

def test_font(request):
    return render(request, "test-font.html", {})

def test_mysql(request):
    tables_info = {}
    try:
        table_names = ['t_article', 't_category', 't_static']
        for table in table_names:
            with connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {table}")
                columns = cursor.fetchall()
                tables_info[table] = columns
    except DatabaseError as error:
        tables_info = {}
        request.session['message'] = "Erreur de connection á la DB. Revenez plus tard."
        request.session['message_status'] = "warning"
        print(f"Database error: {error}")
    return render(request, "test-mysql.html", { 'tables_info': tables_info })

def sponsors(request):
    url = "http://playground.burotix.be/adv/banner_for_isfce.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        formatted_data = pformat(data)
    except requests.exceptions.RequestException as error:
        error = str(error)
        data = []
        formatted_data = []
        request.session['message'] = "Erreur lors de la requete API."
        request.session['message_status'] = "warning"
        print(f"API error: {error}")
    return render(request, "sponsors.html", { 'data': data, 'formatted_data': formatted_data })

def login(request):
    if request.session.get('identified'):
        request.session['message'] = "Vous êtes deja logé, je vous envoie sur votre page utilisateur (user)"
        request.session['message_status'] = "warning"
        return redirect('user')
    else:
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
                    request.session['message'] = f"Vous etes logé en tand que { request.session['role'] }, Bienvenue { request.session['name'] }"
                    request.session['message_status'] = "success"
                    return redirect('user')
                else:
                    request.session['message'] = "Erreur dans le login/password, recommencez..."
                    request.session['message_status'] = "warning"
            else:
                request.session['message'] = f"Code Erreur: { response.status_code }"
                request.session['message_status'] = "warning"
    return render(request, 'login.html')

def user(request):
    if not request.session.get('identified', False):
        request.session['message'] = "Vous devez etre logé pour acceder à cette page"
        request.session['message_status'] = "warning"
        return redirect('login')
    if request.method == 'POST':
        if 'font_color' in request.POST:
            font_color = request.POST.get('font_color', 'black')
            request.session['font_color'] = font_color
            message = "Font color modifié: " + font_color
            return JsonResponse({'success': True, 'message': message})

        elif 'border_style' in request.POST:
            border_style = request.POST.get('border_style', 'none')
            request.session['border_style'] = border_style
            message = "Border style modifié: " + border_style
            return JsonResponse({'success': True, 'message': message})

        elif 'background_color' in request.POST:
            background_color = request.POST.get('background_color', 'whitesmoke')
            request.session['background_color'] = background_color
            message = "Theme modifié: " + background_color
            return JsonResponse({'success': True, 'message': message})

        elif 'home_category' in request.POST:
            home_category = request.POST.get('home_category', 146)
            request.session['home_category'] = home_category
            message = "Categorie modifié: " + home_category
            return JsonResponse({'success': True, 'message': message})

        else:
            request.session.clear()
            request.session['message'] = "Vous venez de vous logout, á bientôt."
            request.session['message_status'] = "success"
            return redirect('home')
    try:
        category = Category.objects.all()
        about = Static.objects.filter(id_sta=1).first()
    except DatabaseError as error:
        category = []
        about = []
        request.session['message'] = "Erreur de connection á la DB. Revenez plus tard."
        request.session['message_status'] = "warning"
        print(f"Database error: {error}")
    return render(request, "user.html", { 'category': category, 'about': about })

def style(request):
    font_color = request.session.get('font_color', 'black')
    border_style = request.session.get('border_style', 'none')
    background_color = request.session.get('background_color', 'whitesmoke')

    border_width = '0px'
    if border_style == 'thin':
        border_width = '2px'
    elif border_style == 'thick':
        border_width = '4px'

    css_content = f"""
    body {{
        background-color: { background_color };
        color: { font_color };
        border: { border_width } solid;
    }}
    """
    return HttpResponse(css_content, content_type='text/css')

def favoris(request):
    # verifie si la personne est logé
    if not request.session.get('identified', False):
        request.session['message'] = "Vous devez être logé pour accéder à cette page"
        request.session['message_status'] = "warning"
        return redirect('login')
    else:
        user_name = request.session.get('name')
        favoris = request.COOKIES.get('favoris', '[]')
        favoris = json.loads(favoris)
        # vérifie si la personne a fait une requete POST
        if request.method == 'POST':
            selected_articles = request.POST.getlist('selected_articles')

            if not selected_articles:
                request.session['message'] = "Vous n'avez pas selectionné d'article á supprimer."
                request.session['message_status'] = "warning"
                return redirect('favoris')

            # creer une nouvelle list vide
            updated_favoris = []
            for item in favoris:
                # vérifie si le favoris doit être gardé (pas selectionné)
                if item['name'] != user_name or item['id_art'] not in selected_articles:
                    updated_favoris.append(item)
            favoris = updated_favoris

            favoris_json = json.dumps(favoris)
            response = redirect('favoris')
            response.set_cookie('favoris', favoris_json)

            request.session['message'] = "Les articles sélectionnés ont été supprimés de vos favoris."
            request.session['message_status'] = "success"
            return response
        else:
            updated_favoris = []
            for item in favoris:
                if item['name'] == user_name:
                    updated_favoris.append(item['id_art'])
            favoris = updated_favoris
            try:
                articles = Article.objects.filter(id_art__in=favoris)
            except DatabaseError as error:
                articles = []
                request.session['message'] = "Erreur de connection á la DB. Revenez plus tard."
                request.session['message_status'] = "warning"
                print(f"Database error: {error}")
            return render(request, 'favoris.html', { 'articles': articles })

def add_favoris(request, id):
    if not request.session.get('identified', False):
        request.session['message'] = "Vous n'avez pas acces á cette page."
        request.session['message_status'] = "warning"
        return render(request, '404.html', status=404)
    else:
        try:
            # verifie si l'id de article existe dans la DB
            if not Article.objects.filter(id_art=id).exists():
                request.session['message'] = f"L'article avec l'ID {id} n'existe pas."
                request.session['message_status'] = "warning"
                return redirect('home')
        except DatabaseError as error:
            request.session['message'] = "Erreur de connection á la DB. Revenez plus tard."
            request.session['message_status'] = "warning"
            print(f"Database error: {error}")
            return redirect('home')

        user_name = request.session.get('name')
        favoris = request.COOKIES.get('favoris', '[]')
        favoris = json.loads(favoris)

        current_favoris = {'name': user_name, 'id_art': str(id)}

        if current_favoris not in favoris:
            favoris.append(current_favoris)
        else:
            request.session['message'] = "Cette articles est déjá present dans vos favoris."
            request.session['message_status'] = "warning"
            return redirect('favoris')
        favoris = json.dumps(favoris)
        response = redirect('article', id=id)
        response.set_cookie('favoris', favoris)
        request.session['message'] = "Cette articles a été rajouté á vos favoris."
        request.session['message_status'] = "success"
        return response

def del_favoris(request, id):
    if not request.session.get('identified', False):
        request.session['message'] = "Vous n'avez pas accés á cette page."
        request.session['message_status'] = "warning"
        return render(request, '404.html', status=404)
    else:
        user_name = request.session.get('name')
        favoris = request.COOKIES.get('favoris', '[]')
        favoris = json.loads(favoris)

        current_favoris = {'name': user_name, 'id_art': str(id)}
        if current_favoris in favoris:
            favoris.remove(current_favoris)
        else:
            request.session['message'] = "Cette article ne se trouve pas dans vos favoris."
            request.session['message_status'] = "warning"
            return redirect('favoris')
        favoris = json.dumps(favoris)
        response = redirect('article', id=id)
        response.set_cookie('favoris', favoris)
        request.session['message'] = "Cette article a été supprimé de vos favoris."
        request.session['message_status'] = "success"
        return response

def date_list(request):
    try:
        dates = Article.objects.values_list('date_art', flat=True).distinct().order_by('-date_art')
    except DatabaseError as error:
        dates = []
        request.session['message'] = "Erreur de connection á la DB. Revenez plus tard."
        request.session['message_status'] = "warning"
        print(f"Database error: {error}")
    return render(request, 'date_list.html', { 'dates' : dates })

def date_list_with_date(request,date):
    try:
        articles = Article.objects.filter(date_art=date).order_by('-date_art')
    except DatabaseError as error:
        articles = []
        request.session['message'] = "Erreur de connection á la DB. Revenez plus tard."
        request.session['message_status'] = "warning"
        print(f"Database error: {error}")
    return render(request, 'date_list.html', { 'articles': articles, 'date_select': date })

def about(request):
    try:
        content = Static.objects.filter(url_sta='about').first()
    except DatabaseError as error:
        content = []
        request.session['message'] = "Erreur de connection á la DB. Revenez plus tard. (about)"
        request.session['message_status'] = "warning"
        print(f"Database error: {error}")
    return render(request, 'about.html', { 'content': content })

def get_recherche_context():
    try:
        category = Category.objects.all()
        max_readtime = Article.objects.all().aggregate(Max('readtime_art'))['readtime_art__max']
        min_readtime = Article.objects.all().aggregate(Min('readtime_art'))['readtime_art__min']
    except DatabaseError as error:
        category = []
        max_readtime = 1
        min_readtime = 1
        request.session['message'] = "Erreur de connection á la DB. Revenez plus tard. (category, readtime)"
        request.session['message_status'] = "warning"
        print(f"Database error: {error}")
    return { 'category': category, 'max_readtime': max_readtime, 'min_readtime': min_readtime }

def get_article_details(request, article_id):
    try:
        article = Article.objects.get(id_art=article_id)
        category_name = article.fk_category_art.name_cat
        nbr_words = len(article.content_art.split())
        data = {
            'id': article.id_art,
            'title': article.title_art,
            'date': article.date_art,
            'category': category_name,
            'readtime': article.readtime_art,
            'nbr_words': nbr_words,
        }
        return JsonResponse(data)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)

def get_recherche_result(request):
    if request.method == "POST":
        try:
            wordTitleArticle = request.POST.get("wordTitleArticle", None)
            wordHookArticle = request.POST.get("wordHookArticle", None)
            wordContentArticle = request.POST.get("wordContentArticle", None)
            dateArticle = request.POST.get("dateArticle", None)
            catArticle = request.POST.get("catArticle", None)
            readTimeArticle = request.POST.get("readTimeArticle", None)
            maxNbrArticle = request.POST.get("maxNbrArticle", "false").lower() == "true"
            nbrArticle = request.POST.get("nbrArticle", None)
            triArticle = request.POST.get("triArticle", "-date_art")
            page = int(request.POST.get("page", 1))

            param_search = {}

            if wordTitleArticle:
                param_search["title_art__icontains"] = wordTitleArticle
            if wordHookArticle:
                param_search["hook_art__icontains"] = wordHookArticle
            if wordContentArticle:
                param_search["content_art__icontains"] = wordContentArticle
            if dateArticle:
                param_search["date_art"] = dateArticle
            if catArticle:
                param_search["fk_category_art"] = catArticle
            if readTimeArticle:
                param_search["readtime_art"] = readTimeArticle

            if maxNbrArticle:
                nbrArticle = None
            else:
                nbrArticle = int(nbrArticle)

            articles = Article.objects.filter(**param_search).order_by(triArticle)[:nbrArticle]
            total_articles = articles.count()
            paginator = Paginator(articles, 10)
            articles = paginator.get_page(page)
            data = {
                "articles": [{"id": art.id_art, "title": art.title_art} for art in articles],
                "page": articles.number,
                "total_pages": paginator.num_pages,
                "total_results": total_articles
            }
            return JsonResponse(data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_session_message(request):
        message = request.session.pop('message', None)
        message_status = request.session.pop('message_status', None)
        return JsonResponse({'message': message, 'message_status': message_status})