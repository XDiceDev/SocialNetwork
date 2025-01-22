from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'), #Первый роут, запускает функцию index из views
    path('get-endpoint-1/', views.get_endpoint_1, name='get_endpoint_1'), # Первый GET эндпоинт
    path('get-endpoint-2/', views.get_endpoint_2, name='get_endpoint_2'), # Второй GET эндпоинт
    path('post-endpoint/', views.post_endpoint, name='post_endpoint'), # POST эндпоинт
    path('single-route/', views.single_route, name='single_route'),  # Единый маршрут

    path('register/', views.register, name='register'), # Регистрация
    path('login/', views.login, name='login'), # Авторизация

    # CRUD пользователя
    # Создание у нас уже есть, оно находится в register
    path('user/<int:user_id>/', views.get_user, name='get_user'), # Чтение
    path('user/update/<int:user_id>/', views.update_user, name='update_user'), # Обновление
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'), # Удаление
]