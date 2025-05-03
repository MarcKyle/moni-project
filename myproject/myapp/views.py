from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
import random
from datetime import datetime, timedelta
from .forms import SimpleTransactionForm, TransactionModelForm
from .models import Transaction

def onboarding(request):
    return render(request, 'onboarding.html')

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
    # Get all transactions for the user
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    # Calculate balance
    balance = 0
    for t in transactions:
        if t.is_added:
            balance += t.amount
        else:
            balance -= t.amount
    # Use the ModelForm for the modal
    form = TransactionModelForm(user=request.user)
    return render(request, 'home.html', {
        'activities': transactions,
        'balance': balance,
        'form': form,
    })

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionModelForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('home')
    else:
        form = TransactionModelForm(user=request.user)
    return render(request, 'add_transaction.html', {'form': form})