import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from .serializers import BookingSerializer


def index(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'bookings': bookings})


class CreateBookingView(APIView):
    def post(self, request):
        # 1. Логируем входящие данные
        print(f"\n[Service A] Получены данные с фронтенда: {request.data}")

        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            payload = serializer.validated_data

            # URL Сервиса Б (проверь порт!)
            SERVICE_B_URL = "https://service-b-j1gc.onrender.com"

            try:
                # 2. Пробуем достучаться до Сервиса Б
                print(f"[Service A] Отправка запроса в Сервис Б: {SERVICE_B_URL}")
                response = requests.post(SERVICE_B_URL, json={
                    "room": payload['room_number'],
                    "start": payload['start_time'].isoformat(),
                    "end": payload['end_time'].isoformat(),
                    "type": payload['booking_type']
                }, timeout=5)

                print(f"[Service A] Ответ от Сервиса Б ({response.status_code}): {response.text}")

                if response.status_code == 200:
                    data_b = response.json()
                    if data_b.get('available'):
                        serializer.save()
                        return Response({"message": "Успешно забронировано!"}, status=201)
                    else:
                        return Response({"error": data_b.get('reason')}, status=400)

                return Response({"error": "Сервис Б отклонил запрос"}, status=response.status_code)

            except requests.exceptions.ConnectionError:
                print("[Service A] ОШИБКА: Сервис Б не запущен на порту 8001")
                return Response({"error": "Сервис Б недоступен (Connection Refused)"}, status=503)
            except Exception as e:
                print(f"[Service A] Непредвиденная ошибка: {e}")
                return Response({"error": str(e)}, status=500)

        # 3. Если данные невалидны (например, пустые поля или не тот формат)
        print(f"[Service A] ОШИБКИ СЕРИАЛИЗАТОРА: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)