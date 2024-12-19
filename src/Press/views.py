from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    print('Bonjour')
    return render(request, "index.html", context={ "name": "Mehdi"})