from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegisterForm
from django.contrib.auth import login

def home(request):
    if request.user.is_authenticated:
        return render(request, "index.html", {"form": UserRegisterForm()})
    return render(request, "index.html", {"form": UserRegisterForm()})

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, "index.html", {"form": form})
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "groups.html")


@login_required
def teacher_dashboard(request):
    return render(request, "teacher.html")

@login_required
def student_dashboard(request):
    return render(request, "student.html")

@login_required
def diet_dashboard(request):
    return render(request, "diet.html")