from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import*
from django.contrib.auth.models import User
# from .models import*
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.conf import settings
import requests
import json
from django.http import JsonResponse


# Create your views here.

def registrationview(request):
    if(request.method=="POST"):
        form = Registerform(request.POST)
        if(form.is_valid()):
            password = form.cleaned_data.get('password')
            cpassword = form.cleaned_data.get('cpassword')
            if(password!=cpassword):
                messages.error(request,'password incorrect')
            else:
                user = form.save(commit=False)
                user.set_password(password)
                user.save()
                messages.success(request,'registration susscess')
                return redirect(loginview)
    else:
        form = Registerform()
    return render(request,'reg.html',{'form':form})

# lofin view
def loginview(request):
    if(request.method=="POST"):
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if(user is not None):
                login(request,user)
                request.session['userid']=user.id
                messages.success(request,f'you  are now logged in as {username}')
                return redirect(index)
            else:
                messages.error(request,'invalid username or password')
        else:
            messages.error(request,'form is not valid')
    else:
        form=AuthenticationForm()
    return render(request,'log.html',{'form':form})

    
# user profile
def userprofile(request):
    id1 =  request.session['userid']
    data = User.objects.get(id=id1)

    db = RecipeModel.objects.all()
    return render(request,'userprofile.html',{'data':data,'db':db})

# profile update
def profile_update(request):
    user = request.user
    if(request.method=="POST"):
        form = Profile_update_form(request.POST,instance=user)
        if form.is_valid(): 
            form.save()
            messages.success(request,'your profile updated succssfully')
            return redirect(userprofile)
    else:
        form = Profile_update_form()
    return render(request,'profileupdate.html',{'form':form})

# index page
def index(request):
    db = RecipeModel.objects.all()
    api_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey":settings.SPOONCULAR_API_KEY,
        "number": 52 ,
        "addRecipeInformation":"false",
        "cuisine":"indian"
    }
    response = requests.get(api_url, params=params)
    recipes = response.json().get('results', []) 
    return render(request,'index.html',{'data':db,'recipes':recipes})


# API
def get_recipe(request):
    api_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey":settings.SPOONCULAR_API_KEY,
        "number": 100,
        "addRecipeInformation":"false",
    }
    response = requests.get(api_url, params=params)
    recipes = response.json().get('results', [])  # Extract recipes or an empty list if none found

    return render(request, 'recipe.html',{'recipes': recipes,})

def get_juice(request):
    api_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey":settings.SPOONCULAR_API_KEY,
        "number":52,
        "query":"juice",
        "addRecipeInformation":"false"
    }
    response = requests.get(api_url, params=params)
    recipes = response.json().get('results',[])
    return render(request,'juice.html',{'recipes':recipes})

# shakes
def get_shakes(request):
    api_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey":settings.SPOONCULAR_API_KEY,
        "query":"shakes",
        "number":52,
        "addRecipeInformation":"false"
        
    }
    response = requests.get(api_url,params= params)
    recipes  = response.json().get('results',[])
    return render(request,'shakes.html',{'recipes':recipes})
    
# coffee
def get_desert(request):
    api_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey":settings.SPOONCULAR_API_KEY,
        "query":"coffee",
        "number":52,
        "addRecipeInformation":"false"
        
    }
    response = requests.get(api_url,params= params)
    recipes  = response.json().get('results',[])
    return render(request,'desert.html',{'recipes':recipes})



# ______________________________________________

# recipe information
def get_recipe_info(request,recipe_id):
    api_url = "https://api.spoonacular.com/recipes/recipe_id/information"
    params = {
        "apiKey":settings.SPOONCULAR_API_KEY
    }
    response =requests.get(api_url,params=params)
    if response.status_code==200:
        recipe_info = response.json()
        return render(request,'recipe_info.html',{'recipe_info':recipe_info})
    else:
        return render(request,'error.html',{"error":'recipe not found'})

    
    

# recipe uploading view

def recipe_uploading(request):
    if(request.method=="POST"):
        images = request.FILES.get('images')
        title = request.POST.get('title')
        ingrediance = request.POST.get('ingrediance', 'Default ingredient text')
        description = request.POST.get('description')
        db = RecipeModel(images=images, title=title, ingrediance=ingrediance, description=description)
        db.save()
        return HttpResponse('uploaded succsfully')
    return render(request,'recipe_upload.html')

# view recipe
def view_recipe(request,id1):
    data = RecipeModel.objects.get(id=id1)
    return render(request,'view_recipe.html',{'data':data})

# update recipe
def update(request,id1):
    data = RecipeModel.objects.get(id=id1)
    if(request.method=="POST"):
        data.images = request.FILES.get('images')
        data.title = request.POST.get('title')
        data.ingrediance = request.POST.get('ingrediance')
        data.description = request.POST.get('description')
        data.save()
        return HttpResponse('recipe updated succssfilly')
    return render(request,'update_recipe.html')
        

# delete recipe
def delete_recipe(request,id1):
    if(request.method=="POST"):
        data = RecipeModel.objects.get(id=id1)
        data.delete()
        return redirect(userprofile)
    return render(request,'delete_recipe.html')


# wishlist view
def add_to_wishlist(request,itemid):
    items = RecipeModel.objects.get(id=itemid)
    wish = WishlistModel.objects.all()
    for i in wish:
        if(i.items == itemid and i.userid==request.session['userid']):
            wish.save()
            return HttpResponse('Item alredy saved in wishlist')
    else:
        db = WishlistModel(userid=request.session['userid'],items= items)
        db.save()
        return redirect(wishlist)
        
def wishlist(request):
 
    db = WishlistModel.objects.all()
    return render(request,'wishlist.html',{'data':db})