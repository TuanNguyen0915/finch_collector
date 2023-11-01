from django.shortcuts import render
from django.http import HttpResponse


class Finch:
    def __init__(self, name, color, description, age):
        self.name = name
        self.color = color
        self.description = description
        self.age = age


finches = [
    Finch("lolo", "yellow", "Kinda rude", 1),
    Finch("fancy", "white", "happy bird", 3),
    Finch("sachi", "green", "angry bird", 2)
]


def finch_index(request):
    return render(request, "finches/index.html", {"finches": finches})


# Create your views here.
def home(request):
    return HttpResponse("<h1>This is home page</h1>")


def about(request):
    return render(request, "about.html")
