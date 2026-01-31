from django.db import models

# Create your models here.
from django.db import models


class Booking(models.Model):
    TYPES = [('lesson', 'Lesson'), ('exam', 'Exam'), ('meeting', 'Meeting')]

    room_number = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    booking_type = models.CharField(max_length=10, choices=TYPES)
    user_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_number} - {self.user_email}"