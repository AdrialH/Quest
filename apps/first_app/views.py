from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import F
from . models import *

import bcrypt

def home(request):

    return render(request, 'first_app/home.html')


def register_page(request):

    return render(request, 'first_app/registration.html')

def login_page(request):

    return render(request, 'first_app/login.html')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if(errors):
        for key, value in errors.items():
            messages.error(request, value)    
        return redirect('/login')
    else:
        if not errors:
            success = {}
            user = User.objects.get(email = request.POST['email'])
            request.session['user'] = user.id
            request.session['first_name']= user.first_name
            for key, value in success.items():
                messages.success(request, value)
        
        return redirect('/logged')

def logged(request):
    errors = {}
    if 'user' not in request.session:
        errors['error'] = "Must register before you can log in."
        if (errors):
            for key, value in errors.items():
                messages.error(request, value)
        return redirect('/index')
    else:
        context = {
            'user': User.objects.get(id = request.session['user']),
            'shop': Shop.objects.all(),
            'mon': Monster.objects.all(),
        }
        return render(request, 'first_app/logged_in.html', context)

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if (errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/index')
    else:
        success = {}
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['firstname'],last_name=request.POST['lastname'], email=request.POST['email'], password = hash1, gold = 100, xp = 0, health = 100)
        success['create'] = "Welcome! You have successfully registered " + request.POST['firstname']
        user = User.objects.get(email = request.POST['email'])
        request.session['user'] = user.id
        request.session['first_name']= user.first_name
        success['success']= "You have been successfully registered, welcome."
        if (success):
            for key, value in success.items():
                messages.success(request, value)
        return redirect('/logged', success)

def create2(request):
   
    errors = Wishlist.objects.wish_validator(request.POST)
    if 'user' not in request.session:
        errors['error'] = "Must register before you can log in."
        return redirect('/')

    else:
        
        if (errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/view')
    
        else:
        
            char = Character.objects.get(id = request.session['user'])
            item = Shop.objects.create(item = request.POST['item'], items_owned = user)
            char.items_owned.add(item)
            return redirect('/logged')

def buyitem(request):
    if 'user' not in request.session:
        errors['error'] = "Must register before you can log in."
        return redirect('/')

    else:
        
        user = User.objects.get(id = request.session['user'])
        item = Shop.objects.get(id = request.POST['item'])
        print('/'*100, item.price)
        user.owned_items.add(item)
        user.gold = F('gold') - item.price
        user.save()
        
        return redirect('/view')

def sellitem(request):
    if 'user' not in request.session:
        errors['error'] = "Must register before you can log in."
        return redirect('/')

    else:

        user = User.objects.get(id = request.session['user'])
        item = Shop.objects.get(id = request.POST['item'])
        print('/'*100, item.price)
        user.owned_items.remove(item)
        user.gold = F('gold') + item.price
        user.save()
        
        return redirect('/view')

def view(request):
    if 'user' not in request.session:
        errors['error'] = "Must register before you can log in."
        return redirect('/')

    else:

        context = {
            'item': Shop.objects.all(),
            'user': User.objects.get(id = request.session['user']),
            
        }
        return render(request, 'first_app/shop.html', context)

def fight(request):
    if 'user' not in request.session:
        errors['error'] = "Must register before you can log in."
        return redirect('/')

    else:

        context = {
            'mon': Monster.objects.get(id = request.POST['mon']),
            'user': User.objects.get(id = request.session['user']) 
        }
        return render(request, 'first_app/quest.html', context)

def attack(request):


    return redirect('/fight')

def logout(request):
    request.session.clear()
    return redirect('/')

def goback(request):
    if 'user' not in request.session:
        errors['error'] = "Must register before you can log in."
        return redirect('/')

    else:

        return redirect('/logged')

def delete(request):
    b= User.objects.get(id = request.POST['item'])
    b.delete()
    return redirect('/logged')
    