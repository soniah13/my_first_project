from django.shortcuts import render, redirect, get_object_or_404
from .models import  Meal
from .forms import  Mealform
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages


# Create your views here.
# these are the views for adding, viewing added meals, remove food, reset calorie count

# user will need to be login in the be able to do the following functions
@login_required(login_url='login_user')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='login_user')
def add_meal(request):
    if request.method == 'POST':
        meal_form = Mealform(request.POST)
        if meal_form.is_valid():
            meal = meal_form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect('meal_list')
    else:
        meal_form = Mealform()  #intialise the get request
    return render(request, 'add_meal.html', 
                  {'meal_form': meal_form})


@login_required(login_url='login_user')     #user will be getting a display message everytime the calories are to be reset
def meal_list(request):
    meals = Meal.objects.filter(user=request.user)

    # group meal by type and sum calories
    breakfast_caloies =  sum(meal.total_calories for meal in meals if meal.meal_type == 'breakfast') 
    lunch_calories = sum(meal.total_calories for meal in meals if meal.meal_type == 'lunch')
    dinner_calories = sum(meal.total_calories for meal in meals if meal.meal_type == 'dinner')

    return render(request, 'meal_list.html', {
        'meals': meals,
        'breakfast_calories': breakfast_caloies,
        'lunch_calories': lunch_calories,
        'dinner_calories': dinner_calories,
    }) 


@login_required(login_url='login_user')
def remove_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    meal.delete()
    return redirect('meal_list')


@login_required(login_url='login_user')
def reset_calories(request, meal_type):
    meals = Meal.objects.filter(user=request.user, meal_type=meal_type)
    for meal in meals:
        meal.calories_reset = True
        meal.total_calories = 0
        meal.save()
    return redirect('meal_list')


def register_user(request):
   form = CreateUserForm()
   if request.method == 'POST':
       form = CreateUserForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('login_user')
   context = {'registerform': form}
   return render(request, 'register_user.html', context=context)
   


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')
    context = {'loginform':form}
    
    return render(request, 'login_user.html', context=context )


@login_required(login_url='login_user')
def logout_user(request):
    auth.logout(request)
    messages.success(request, ('You are now logged out..'))
    return redirect(request, '')

