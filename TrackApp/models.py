from django.db import models
from django.contrib.auth.models import User

class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]

    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()  # Specify a default value here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_calories = models.PositiveIntegerField()
    calories_reset = models.BooleanField(default=False)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, default='breakfast')

    def calculate_total_calories(self):
        self.total_calories = self.calories + self.calories
        self.save()
        

    def reset_calories(self):
        self.calories_reset = True
        self.total_calories = 0
        self.save()

    def __str__(self):
        return self.name
    


    