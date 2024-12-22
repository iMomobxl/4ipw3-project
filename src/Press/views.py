from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    print('Test views')
    return render(request, "index.html", context={ "name": "Mehdi" })