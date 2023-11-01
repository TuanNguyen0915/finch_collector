from django.db import models
from django.urls import reverse


# Create your models here.


class Finch(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("finch-detail", kwargs={"finch_id": self.id})


MEALS = (("B", "Breakfast"), ("L", "Lunch"), ("D", "Dinner"))


class Feeding(models.Model):
    date = models.DateField()
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.get_meal_display()} on {self.date}"
