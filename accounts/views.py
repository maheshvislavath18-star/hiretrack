from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile


# 🔥 Home Page
def home(request):
    return render(request, "accounts/home.html")


# 🔥 Register
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # check user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect('register')

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ✅ Create profile automatically
        Profile.objects.get_or_create(user=user)

        messages.success(request, "Account created successfully ✅")
        return redirect('login')

    return render(request, 'accounts/register.html')


# 🔥 Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password ❌")
            return redirect('login')

    return render(request, 'accounts/login.html')


# 🔥 Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# 🔥 Dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = Profile.objects.get(user=request.user)
    return render(request, "accounts/dashboard.html", {"profile": profile})


# 🔥 Edit Profile
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST.get("phone")
        profile.location = request.POST.get("location")
        profile.save()
        messages.success(request, "Profile updated ✅")
        return redirect("dashboard")

    return render(request, "accounts/edit_profile.html", {"profile": profile})


# 🔥 Test Insert (only for practice)
def insert_profile(request):
    user = User.objects.first()

    if not user:
        return HttpResponse("No user found ❌")

    Profile.objects.create(
        user=user,
        phone="9876543210",
        location="Hyderabad"
    )

    return HttpResponse("Profile Inserted Successfully ✅")