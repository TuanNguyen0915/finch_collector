from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch


# Create your views here.
class FinchCreate(CreateView):
    model = Finch
    fields = ["name", "color", "description", "age"]
    success_url = "/finches/"


class FinchUpdate(UpdateView):
    model = Finch
    fields = ["name", "color", "description", "age"]


class FinchDelete(DeleteView):
    model = Finch
    success_url = "/finches/"


def home(request):
    return render(request, "home.html")


def finch_index(request):
    finches = Finch.objects.all()
    return render(request, "finches/index.html", {"finches": finches})


def finch_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, "finches/detail.html", {"finch": finch})


def about(request):
    return render(request, "about.html")
