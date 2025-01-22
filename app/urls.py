from django.urls import path
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'), #Первый роут, запускает функцию index из views
    path('get-endpoint-1/', views.get_endpoint_1, name='get_endpoint_1'), # Первый GET эндпоинт
    path('get-endpoint-2/', views.get_endpoint_2, name='get_endpoint_2'), # Второй GET эндпоинт
    path('post-endpoint/', views.post_endpoint, name='post_endpoint'), # POST эндпоинт
    path('single-route/', views.single_route, name='single_route'),  # Единый маршрут

    path('register/', views.register, name='register'), # Регистрация
    path('login/', views.login_view, name='login'), # Авторизация

    # CRUD пользователя
    # Создание у нас уже есть, оно находится в register
    path('user/<int:user_id>/', views.get_user, name='get_user'), # Чтение
    path('user/update/<int:user_id>/', views.update_user, name='update_user'), # Обновление
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'), # Удаление

    path('profile/', views.profile, name='profile'), # Страница профиля
    path('logout/', views.logout_view, name='logout'), # Выход из аккаунта
    path('delete-account/', views.delete_account, name='delete_account'), # Удалить аккаунт
    path('edit-profile/', views.edit_profile, name='edit_profile'), # Редактировать профиль
    path('confirm-email/<str:token>/', views.confirm_email, name='confirm_email'), # Подтверждение почты

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]