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
    if request.method == 'POST': #Проверяем, POST ли запрос
        try:
            data = json.loads(request.body) #Загружаем данные из запроса из Json
            username = data.get('username')
            password = data.get('password')
            if not username or not password: #Если нет имени или пароля
                return JsonResponse({"error": "Требуется имя и пароль"}) #Возвращаем Json с "ошибкой"
            
            if User.objects.filter(username=username).exists(): #Если имя уже занято
                return JsonResponse({"error": "Имя уже занято"}) #Возвращаем Json с "ошибкой"

            user = User.objects.create_user(username=username, password=password) #Создаем сущность пользователя
            return JsonResponse({"message": "Регистрация прошла успешно"}) #Возвращаем Json о том, что все прошло успешно
        except Exception as e:
            return JsonResponse({"error": str(e)}) #Если произошла какая либо еще ошибка - возвращаем ее
    return JsonResponse({"error": "Разрешены только POST запросы"}) #Возвращаем Json с "ошибкой"

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password) #Проходим аутентификацию
            if user is not None: #Если прошли (user не null) (извините, я эти None не могу читать нормально, у меня C# головного мозга))))))
                login(request, user) #Логинимся
                return JsonResponse({"message": "Вход прошел успешно"})
            return JsonResponse({"error": "Неверное имя пользователя или пароль"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Разрешены только POST запросы"})



def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            "id": user.id,
            "username": user.username,
        })
    except User.DoesNotExist: #Если пользователя не существует
        return JsonResponse({"error": "Пользователь не найден"})

@csrf_exempt
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=user_id)

            username = data.get('username')
            
            if username:
                user.username = username
            
            user.save()
            return JsonResponse({"message": f"Имя {user.username} успешно обновлено"})
        except User.DoesNotExist:
            return JsonResponse({"error": "Пользователь не найден"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Разрешены только PUT запросы"})

@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({"message": "Пользователь удален успешно"})
        except User.DoesNotExist:
            return JsonResponse({"error": "Пользователь не найден"})
    return JsonResponse({"error": "Разрешены только DELETE запросы"})