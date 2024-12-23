import csv, os
from django.conf import settings

def display_menu_csv():
    menu_items = []
    csv_path = os.path.join(settings.BASE_DIR, 'asset', 'menu.csv')
    with open(csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter='|')
        for row in csv_reader:
            menu_items.append({'id': row['id'], 'name': row['name']})
    return menu_items

def menu_items(request):
    return { 'menu_items': display_menu_csv() }