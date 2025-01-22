from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def index(request):
    return HttpResponse("Тестовая страница") #Возвращает http ответ с текстом "Тестовая страница"

def get_endpoint_1(request):
    return HttpResponse("Это первый GET эндпоинт")

def get_endpoint_2(request):
    return HttpResponse("Это второй GET эндпоинт")

@csrf_exempt #Отключает проверку CSRF, чтобы тестировать запросы
def post_endpoint(request):
    if request.method == 'POST':
        data = {"message": "POST запрос"}
        return JsonResponse(data)
    return JsonResponse({"message": "Неправильный метод запроса"})

@csrf_exempt
def single_route(request):
    if request.method == 'GET':
        return HttpResponse("Это GET запрос в /single-route")
    elif request.method == 'POST':
        return HttpResponseRedirect('/') # Редирект при POST-запросе
    else:
        return HttpResponse("Неправильный метод запроса")
    
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({"error": "Требуется имя и пароль"})
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Имя уже занято"})

            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({"message": "Регистрация прошла успешно"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Разрешены только POST запросы"})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Вход прошел успешно"})
            return JsonResponse({"error": "Неверное имя пользователя или пароль"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Разрешены только POST запросы"})

    #Думаю выше тут все очевидно