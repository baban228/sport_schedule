# config/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import sys


def home(request):
    """Главная страница — только отображение, без обработки форм"""
    # Передаём пустую форму регистрации как reg_form (чтобы не конфликтовала с формой входа)
    return render(request, "index.html", {"reg_form": UserRegisterForm()})


def login_view(request):
    """Обработчик входа через модалку (POST на /login/)"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"🔐 [LOGIN] Попытка входа: username={username}", flush=True, file=sys.stdout)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"✅ [LOGIN] Успех: {user.username}", flush=True, file=sys.stdout)
            login(request, user)
            return redirect("home")
        else:
            print("❌ [LOGIN] Ошибка: неверные данные", flush=True, file=sys.stdout)
            messages.error(request, "❌ Неверное имя пользователя или пароль")
            return redirect("home")
    
    # GET на /login/ — просто редирект на главную
    return redirect("home")


def register_view(request):
    """Обработчик регистрации"""
    if request.method == "POST":
        print("📝 [REGISTER] Получен POST-запрос", flush=True, file=sys.stdout)
        print(f"📝 [REGISTER] POST keys: {list(request.POST.keys())}", flush=True, file=sys.stdout)
        
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            print("✅ [REGISTER] Валидация прошла успешно", flush=True, file=sys.stdout)
            print(f"✅ [REGISTER] Cleaned data keys: {list(form.cleaned_data.keys())}", flush=True, file=sys.stdout)
            
            # Создаём пользователя, но не сохраняем в БД сразу
            user = form.save(commit=False)
            
            # Получаем пароль: приоритет cleaned_data, фоллбэк на POST
            password = form.cleaned_data.get('password')
            if not password:
                password = request.POST.get('password')
            
            if password:
                print("🔐 [REGISTER] Хеширую пароль...", flush=True, file=sys.stdout)
                user.set_password(password)  # ← КРИТИЧНО: хешируем перед сохранением!
            else:
                print("⚠️ [REGISTER] Пароль не найден в данных!", flush=True, file=sys.stdout)
            
            # Сохраняем в БД
            user.save()
            print(f"✅ [REGISTER] Пользователь создан: id={user.id}, username={user.username}, role={user.role}", flush=True, file=sys.stdout)
            
            # Автоматический вход после регистрации
            login(request, user)
            print("✅ [REGISTER] Авторизация успешна. Редирект.", flush=True, file=sys.stdout)
            return redirect('home')
        else:
            # 🔴 Валидация не прошла — выводим детали для отладки
            print("❌ [REGISTER] ОШИБКИ ФОРМЫ:", form.errors, flush=True, file=sys.stdout)
            # Безопасный вывод POST-данных (скрываем пароль)
            safe_post = {k: ('***' if 'password' in k.lower() else v) for k, v in request.POST.items()}
            print("❌ [REGISTER] POST данные:", safe_post, flush=True, file=sys.stdout)
    else:
        print("🔹 [REGISTER] GET-запрос. Отдаю пустую форму.", flush=True, file=sys.stdout)
        form = UserRegisterForm()
    
    # Возвращаем страницу с формой (ошибки будут видны в шаблоне через reg_form.errors)
    return render(request, "index.html", {"reg_form": form})


def is_admin(user):
    """Проверка роли администратора"""
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