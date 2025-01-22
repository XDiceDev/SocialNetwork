from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'), #Первый роут, запускает функцию index из views
    path('get-endpoint-1/', views.get_endpoint_1, name='get_endpoint_1'), # Первый GET эндпоинт
    path('get-endpoint-2/', views.get_endpoint_2, name='get_endpoint_2'), # Второй GET эндпоинт
    path('post-endpoint/', views.post_endpoint, name='post_endpoint'), # POST эндпоинт
    path('single-route/', views.single_route, name='single_route'),  # Единый маршрут
]