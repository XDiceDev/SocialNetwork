from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

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