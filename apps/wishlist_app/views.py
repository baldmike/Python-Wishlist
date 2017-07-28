from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect, reverse
from models import *
from django.contrib import messages
import bcrypt

def index(request):

    return render(request, 'wishlist_app/index.html')

def register(request):

    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.add_message(request, messages.ERROR, errors[tag])
        return redirect("/")
    else:
        first_name =  request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
 
        user = User.objects.create_user(first_name, last_name, email, hashed_password)

        if not user:
            messages.add_message(request, messages.ERROR, "User email already exists.")
            return redirect("/")
        else:
            request.session['first_name'] = first_name
            request.session['user_id'] = user.id

            return redirect('/home')

def login(request):
    try:
        user = User.objects.login_validator(request.POST)

        if user:
            request.session['first_name'] = user.first_name
            request.session['user_id'] = user.id
            return redirect('/home')
        else:
            messages.add_message(request, messages.ERROR, "Invalid login info.")
            return redirect("/")
    except:
        messages.add_message(request, messages.ERROR, "Not in database")
        return redirect('/')

def addItem(request):
    user = request.session['user_id']

    if request.method == 'POST':
        item_name = request.POST['item_name']
        Item.objects.create(item_name=item_name, added_by_id=user)

        return redirect ('/home')

    return redirect ('/home')

def home(request):
    user = request.session['user_id']
    
    context = {

        'allItems': Item.objects.all().exclude(item_additions__user_id=user),
        'myItems': Addition.objects.filter(user_id=user)

    }

    return render(request, 'wishlist_app/home.html', context)

def addToMyItems(request, item_id):
        
    Addition.objects.create(item_id=item_id, user_id=request.session['user_id'])
    
    return redirect ('/home')

def addToWishlist(request):
    user = request.session['user_id']
    
    context = {

        'allItems': Item.objects.all().exclude(item_additions__user_id=user),
        'myItems': Addition.objects.filter(user_id=user)

    }

    return render(request, 'wishlist_app/addItem.html', context)

def deleteItem(request, item_id):
    user = request.session['user_id']

    item = Addition.objects.get(item_id=item_id, user_id=user)
    item.delete()

    return redirect ('/home')

def items(request, item_id):

    all_users = Addition.objects.filter(item_id=item_id)
    print all_users
    
    context = {

        'all_users': all_users,
    
    }

    return render(request, 'wishlist_app/items.html', context)
    

def reset(request):
    request.session.flush()
    return redirect('/')