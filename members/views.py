from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
#from .models import *

from store.models import *
from store.utils import cookieCart, cartData, guestOrder


#from .utils import cookieCart, cartData, guestOrder

def login_user(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products' : products, 'cartItems' : cartItems}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
            ...
        else:
            messages.success(request, ("There Was An Error Loggin in, Try Again..."))
            return redirect('login')
            ...
    else:
        return render(request, 'authenticate/login.html', context)

def logout_user(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products' : products, 'cartItems' : cartItems}
    logout(request)
    messages.success(request, ("You Were Logged Out."))

    return redirect('store')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
            
        # add cart data ->
        data = cartData(request)
        cartItems = data['cartItems']

        products = Product.objects.all()
        context = {'products' : products, 'cartItems' : cartItems}
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)

            Customer.objects.create(
                user = user,
                name=user.username,
                email = email,
            )
            
            login(request,user)
            
            messages.success(request, ("Registered successfully!"))
            return redirect('store')
        
    else :
        form = RegisterUserForm()

    context = {'form': form,}
    return render(request, 'authenticate/register.html', context)