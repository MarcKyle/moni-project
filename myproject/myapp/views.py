from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
import random
from datetime import datetime, timedelta

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords don't match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create the user and save the firstname and lastname
        user = User.objects.create_user(username=username, password=password1, email=email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate using the custom backend
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
    return render(request, 'login.html')
 

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    
    # Simulate some random activities and balance for the user
    activities = []
    num_activities = random.randint(3, 10) 
    balance = 0 

    for _ in range(num_activities):
        amount = random.randint(1, 1000)
        is_added = random.choice([True, False])  
        timestamp = datetime.now() - timedelta(minutes=random.randint(1, 1440))

        # Update balance based on activity
        if is_added:
            balance += amount
        else:
            balance -= amount

        activities.append({
            'amount': amount,
            'is_added': is_added,
            'timestamp': timestamp,
        })

    return render(request, 'home.html', {'activities': activities, 'balance': balance})