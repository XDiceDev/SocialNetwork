from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import send_confirmation_email, confirm_email_token
from django.shortcuts import get_object_or_404
from .models import Profile

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
    


def register(request):
    if request.method == 'POST': #Проверяем, POST ли запрос
        username = request.POST['username'] #Получаем данные
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'register.html', {"error": "Пароли не совпадают"})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {"error": "Имя пользователя уже используется"})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {"error": "Email уже используется"})

        try:
            user = User.objects.create_user(username=username, email=email, password=password1) #Создаем сущность пользователя
            user.save() #Сохраняем
            Profile.objects.get_or_create(user=user)
            send_confirmation_email(user) #Отправляем подтверждение почты
            return render(request, 'register.html', {"success": "На вашу почту отправлено письмо для подтверждения"})
        except Exception as e:
            return render(request, 'register.html', {"error": f"Ошибка регистрации: {str(e)}"})
    
    return render(request, 'register.html')

def login_view(request): #Пришлось поменять название чтобы не коллайдилось с login из django
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) #Проходим аутентификацию

        if user is not None: #Если прошли
            if user.profile.is_email_verified:
                login(request, user) #Логинимся
                return redirect('profile') #Перенаправление на профиль
            else:
                return render(request, 'login.html', {"error": "Почта не подтверждена"})
        else:
            return render(request, 'login.html', {"error": "Неверные данные"})
    
    return render(request, 'login.html')



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



@login_required
def profile(request):
    return render(request, 'profile.html') #Просто показываем профиль

def logout_view(request):
    logout(request) #Выходим из аккаунта
    return redirect('login') #Редирект на вход

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete() # Удаляем пользователя
        return redirect('login') #Редирект на вход

@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST['username']

        user = request.user
        user.username = username
            
        user.save()
        return redirect('profile')

    return render(request, 'edit_profile.html')

def confirm_email(request, token):
    email = confirm_email_token(token)
    if email:
        user = get_object_or_404(User, email=email)
        user.profile.is_email_verified = True
        user.profile.save()
        return render(request, 'confirm_email.html', {"success": "Email успешно подтвержден"})
    else:
        return render(request, 'confirm_email.html', {"error": "Неверный или истекший токен"})