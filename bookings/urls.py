from django.urls import path
from .views import index, CreateBookingView

urlpatterns = [
    # Главная страница с веб-интерфейсом
    path('', index, name='index'),

    # API-endpoint для создания бронирования
    path('api/create-booking/', CreateBookingView.as_view(), name='create_booking'),
]