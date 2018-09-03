
from django.shortcuts import render


def index(request):
    return render(request, "pur_beurre/pages/home.html")


def results(request):
    return render(request, "pur_beurre/pages/results.html")


def food(request):
    return render(request, "pur_beurre/pages/food.html")


def legal(request):
    return render(request, "pur_beurre/pages/legal.html")
