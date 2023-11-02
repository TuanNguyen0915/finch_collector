from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Finch, Toy
from .form import FeedingForm


# Create your views here.
class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ["name", "color", "description", "age"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ["name", "color", "description", "age"]


class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = "/finches/"


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ["name", "color"]
    success_url = "/toys"


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = "/toys/"


class Home(LoginView):
    template_name = "home.html"


@login_required
def finch_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, "finches/index.html", {"finches": finches})


@login_required
def finch_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    feeding_form = FeedingForm()
    toy_finch_doesnt_have = Toy.objects.exclude(
        id__in=finch.toys.all().values_list("id")
    )
    return render(
        request,
        "finches/detail.html",
        {"finch": finch, "feeding_form": feeding_form, "toys": toy_finch_doesnt_have},
    )


def about(request):
    return render(request, "about.html")


@login_required
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect("finch-detail", finch_id=finch_id)


@login_required
def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect("finch-detail", finch_id=finch_id)


def signup(request):
    error_message = ""
    if request.method == "POST":
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect("finch-index")
        else:
            error_message = "Invalid sign up - try again"
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "signup.html", context)
    # Same as: return render(request, 'signup.html', {'form': form, 'error_message': error_message})
