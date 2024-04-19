from django.contrib.auth.context_processors import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, AddRecipeForm, EditRecipeForm, UploadRecipeImageForm
from .models import Recipe, Categories, RecipeCategory
from django.core.files.storage import FileSystemStorage


# Create your views here.
def home(request):
    random_recipes = Recipe.objects.order_by('?')[:5]
    context = {'recipes_list': random_recipes, 'title': 'Home'}
    if request.user.is_authenticated:
        context['is_authenticated'] = True
    return render(request, 'recipes_app/home.html', context)


def recipe_page(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    context = {'recipe': recipe, 'title': recipe.title}
    if recipe.author.username == request.user.username:
        context['is_author'] = True
    if request.user.is_authenticated:
        context['is_authenticated'] = True
    return render(request, 'recipes_app/recipe_page.html', context)


def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['recipe_title']
            category = form.cleaned_data['recipe_category']
            description = form.cleaned_data['recipe_description']
            steps = form.cleaned_data['recipe_steps']
            cooking_time = form.cleaned_data['recipe_cooking_time']
            new_recipe = Recipe(title=title,
                                description=description, steps=steps,
                                cooking_time=cooking_time,
                                author=request.user)
            category_instance = Categories.objects.filter(pk=category).first()
            recipe_category = RecipeCategory(category=category_instance, recipe=new_recipe)
            new_recipe.save()
            recipe_category.save()
            return redirect('upload_image', recipe_id=new_recipe.id)
    else:
        form = AddRecipeForm()
        context = {'form': form, 'title': 'Новый рецепт', 'is_authenticated': True}
        return render(request, 'recipes_app/add_recipe.html', context=context)


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
            return render(request, 'recipes_app/recipe_page.html', {'recipe': recipe, 'is_authenticated': True})
    else:
        form = UploadRecipeImageForm()
        context = {'form': form, 'title': 'Загрузка изображения', 'is_authenticated': True}
        return render(request, 'recipes_app/upload_recipe_img.html', context)


def edit_recipe(request, recipe_id):
    if request.method == 'POST':
        form = EditRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe_title = form.cleaned_data['recipe_title']
            recipe_category = form.cleaned_data['recipe_category']
            recipe_description = form.cleaned_data['recipe_description']
            recipe_steps = form.cleaned_data['recipe_steps']
            recipe_cooking_time = form.cleaned_data['recipe_cooking_time']
            recipe = Recipe.objects.get(pk=recipe_id)
            if recipe_title != '':
                recipe.title = recipe_title
            if recipe_description != '':
                recipe.description = recipe_description
            if recipe_steps != '':
                recipe.steps = recipe_steps
            if recipe_cooking_time is not None:
                recipe.cooking_time = recipe_cooking_time
            recipe.save()
            category_instance = Categories.objects.filter(pk=recipe_category).first()
            current_category = RecipeCategory.objects.get(recipe=recipe_id)
            if category_instance != current_category.category:
                previous_category = RecipeCategory.objects.filter(recipe=recipe_id).first()
                previous_category.delete()
                category = RecipeCategory(category=category_instance, recipe=recipe)
                category.save()
            return redirect('upload_image', recipe_id=recipe_id)
    else:
        recipe = Recipe.objects.get(pk=recipe_id)
        current_category = RecipeCategory.objects.get(recipe=recipe_id)
        form = EditRecipeForm()
        context = {'form': form, 'title': 'Редактирование', 'is_authenticated': True, 'recipe': recipe,
                   'current_category': current_category}
        return render(request, 'recipes_app/edit_recipe.html', context)


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
                    return HttpResponse('Неверное имя пользователя или пароль')
    else:
        form = LoginForm()
        context = {'form': form, 'title': 'Вход'}
        return render(request, 'recipes_app/log_in.html', context)


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
                return HttpResponse('Такой пользователь уже существует')
            if User.objects.filter(email=email).exists():
                return HttpResponse('Такой электронный адрес уже зарегистрирован')
            if password != confirm_password:
                return HttpResponse('Пароли не совпадают')
            new_user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
            new_user.save()
            return redirect('log_in')
    else:
        form = RegistrationForm()
        context = {'form': form, 'title': 'Регистрация'}
        return render(request, 'recipes_app/registration.html', context)


def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('log_in')
    else:
        context = {'title': 'Выход'}
        return render(request, 'recipes_app/log_out.html', context={'title': 'Logout'})


def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    context = {'recipes_list': recipes, 'title': 'Мои рецепты', 'is_authenticated': True}
    return render(request, 'recipes_app/my_recipes.html', context)


def categories_view(request):
    categories = Categories.objects.all()
    context = {'categories': categories, 'title': 'Категории рецептов'}
    if request.user.is_authenticated:
        context['is_authenticated'] = True
    return render(request, 'recipes_app/categories.html', context)


def category_recipes(request, category_id):
    recipes_list = RecipeCategory.objects.filter(category=category_id)
    recipes = []
    for item in recipes_list:
        recipes.append(item.recipe)
    title = Categories.objects.get(pk=category_id).title
    context = {'recipes_list': recipes, 'title': title}
    if request.user.is_authenticated:
        context['is_authenticated'] = True
    return render(request, 'recipes_app/category_recipes.html', context)
