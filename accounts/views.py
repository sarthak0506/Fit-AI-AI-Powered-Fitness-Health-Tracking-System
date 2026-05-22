from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username  = request.POST['username']
        email     = request.POST['email']
        password  = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/signup.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('profile')
    return render(request, 'accounts/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.age           = int(request.POST.get('age', 25))
        profile.weight_kg     = float(request.POST.get('weight_kg', 70))
        profile.height_cm     = float(request.POST.get('height_cm', 170))
        profile.gender        = request.POST.get('gender', 'male')
        profile.activity_days = int(request.POST.get('activity_days', 3))
        profile.goal          = request.POST.get('goal', 'maintain')
        profile.diet_pref     = request.POST.get('diet_pref', 'veg')
        profile.supplements   = request.POST.get('supplements') == 'on'
        profile.location      = request.POST.get('location', 'gym')
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profile updated!')
        return redirect('dashboard')
    return render(request, 'accounts/profile.html', {'profile': profile})