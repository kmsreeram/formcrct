from itertools import product

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages

from .forms import ProductForm
from .models import Products, Category, Cart


def base(request):
    product = Products.objects.all()
    return render(request, 'base.html', {'product': product})

def index(request):
    return render(request,'index.html')

def add_product(request):
    if request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES)
        if productform.is_valid():
            productform.save()
            productform = ProductForm()  # Reset the form after saving
            return render(request, 'add_product.html', {'form': productform})
    else:
        productform = ProductForm()  # Initialize an empty form for GET request
    return render(request, 'add_product.html', {'form': productform})

def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('base')
    else:
        product_form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': product_form})

def delete_product(request, pk):
    product = get_object_or_404(Products, pk=pk)
    product.delete()
    return redirect('base')

def product_detail(request, id):
    product = get_object_or_404(Products, id=id)
    return render(request, 'product_detail.html', {'product': product})

def products(request):
    product = Products.objects.all()
    return render(request, 'products.html', {'product': product})

def signup(request):
    if request.method=='POST':
        username = request.POST['username']
        fname = request.POST['username']
        lname = request.POST['fname']
        email = request.POST['email']
        password1 = request.POST['password1']

        myuser=User.objects.create_user(username=username,password=password1,email=email)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        return redirect('signin')
    return render(request,'signup.html')

def signin(request):
    if request.method =='POST':
        username=request.POST['username']
        password1=request.POST['password1']
        user=authenticate(username=username,password=password1)
        if user is not None:
            login(request, user)
            fname=user.first_name
            lname=user.last_name
            return render(request,'user_dashboard.html',{'fname':fname,'lname':lname})
        else:
            messages.error(request," login again")
            return redirect('signin')
    return render(request,'signin.html')

def signout(request):
    logout(request)
    return render(request,'base.html')

def buy_now(request):
    return render(request,'buy_now.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 2
    cart_item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

@login_required
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_view')


