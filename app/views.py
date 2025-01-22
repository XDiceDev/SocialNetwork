from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Тестовая страница") #Возвращает http ответ с текстом "Тестовая страница"