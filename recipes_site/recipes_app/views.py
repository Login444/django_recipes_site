from django.contrib.auth.context_processors import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, AddRecipeForm, EditRecipeForm, UploadRecipeImageForm
from .models import Recipe, RecipeCategory, Categories
from django.core.files.storage import FileSystemStorage


# Create your views here.
def home(request):
    recipes_list = Recipe.objects.all()
    context = {'recipes_list': recipes_list, 'title': 'Home'}
    if request.user.is_authenticated:
        context['is_authenticated'] = True
    return render(request, 'recipes_app/home.html', context)


def recipe_page(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    context = {'recipe': recipe, 'title': recipe.title}
    if recipe.author.username == request.user.username:
        context['is_author'] = True
    return render(request, 'recipes_app/recipe_page.html', context)


def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe_title = form.cleaned_data['recipe_title']
            recipe_category = form.cleaned_data['recipe_category']
            recipe_description = form.cleaned_data['recipe_description']
            recipe_steps = form.cleaned_data['recipe_steps']
            recipe_cooking_time = form.cleaned_data['recipe_cooking_time']
            new_recipe = Recipe(title=recipe_title,
                                description=recipe_description, steps=recipe_steps,
                                cooking_time=recipe_cooking_time,
                                author=request.user)
            new_recipe.save()
            return redirect('upload_image', recipe_id=new_recipe.id)
    else:
        form = AddRecipeForm()
        return render(request, 'recipes_app/add_recipe.html',
                      {'form': form, 'title': 'Add recipe', 'is_authenticated': True})


def upload_image(request, recipe_id):
    if request.method == 'POST':
        form = UploadRecipeImageForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = Recipe.objects.get(pk=recipe_id)
            image = form.cleaned_data['image']
            recipe.photo = image
            recipe.save()
            file = FileSystemStorage()
            file.save(name=image.name, content=image)
            return render(request, 'recipes_app/recipe_page.html', {'recipe': recipe})
    else:
        form = UploadRecipeImageForm()
        return render(request, 'recipes_app/upload_recipe_img.html', {'form': form,
                                                                      'title': 'Upload image', 'is_authenticated': True})


def edit_recipe(request, recipe_id):
    if request.method == 'POST':
        form = EditRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe_title = form.cleaned_data['recipe_title']
            recipe_description = form.cleaned_data['recipe_description']
            recipe_steps = form.cleaned_data['recipe_steps']
            recipe_cooking_time = form.cleaned_data['recipe_cooking_time']
            recipe_photo = form.cleaned_data['recipe_photo']
            recipe = Recipe.objects.get(pk=recipe_id)
            recipe.recipe_title = recipe_title
            recipe.recipe_description = recipe_description
            recipe.recipe_steps = recipe_steps
            recipe.recipe_cooking_time = recipe_cooking_time
            recipe.recipe_photo = recipe_photo
            recipe.save()
            file = FileSystemStorage()
            file.save(recipe_photo.name, recipe_photo)
            return render(request, 'recipes_app/recipe_page.html', {'recipe': recipe})
    else:
        form = EditRecipeForm()
        return render(request, 'recipes_app/edit_recipe.html',
                      {'form': form, 'title': 'Edit recipe', 'is_authenticated': True})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if user.check_password(password):
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Invalid username or password')
    else:
        form = LoginForm()
        return render(request, 'recipes_app/log_in.html', {'form': form, 'title': 'Login'})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if User.objects.filter(username=username).exists():
                return HttpResponse('User already exists')
            if User.objects.filter(email=email).exists():
                return HttpResponse('Email already registered')
            if password != confirm_password:
                return HttpResponse('Passwords do not match')
            new_user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
            new_user.save()
            return redirect('log_in')
    else:
        form = RegistrationForm()
        return render(request, 'recipes_app/registration.html', {'form': form, 'title': 'Register'})


def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('log_in')
    else:
        return render(request, 'recipes_app/log_out.html', context={'title': 'Logout'})


def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipes_app/my_recipes.html',
                  {'recipes_list': recipes, 'title': 'My Recipes', 'is_authenticated': True})







