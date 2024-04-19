from django import forms

from .models import Categories


class RegistrationForm(forms.Form):
    user_name = forms.CharField(label='Имя пользователя (Ваш Логин)', max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', max_length=150,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Адрес электронной почты',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Придумайте пароль', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Повторите пароль', max_length=100,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    user_name = forms.CharField(label='Ваш Логин', max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Ваш пароль', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddRecipeForm(forms.Form):
    @staticmethod
    def category_choices():
        categories = Categories.objects.all()
        choices_list = []
        for category in categories:
            res_tuple = (category.id, category.title)
            choices_list.append(res_tuple)
        return choices_list

    recipe_title = forms.CharField(label='Название', max_length=150,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipe_category = forms.ChoiceField(label='Категория', choices=category_choices(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    recipe_description = forms.CharField(label='Краткое описание', max_length=800,
                                         widget=forms.Textarea(attrs={'class': 'form-control'}))
    recipe_steps = forms.CharField(label='Шаги приготовления', max_length=2000,
                                   widget=forms.Textarea(attrs={'class': 'form-control'}))
    recipe_cooking_time = forms.IntegerField(label='Время приготовления (в минутах)', min_value=1,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))


class UploadRecipeImageForm(forms.Form):
    image = forms.ImageField(label='Загрузите изображение', widget=forms.FileInput(attrs={'class': 'form-control'}))


class EditRecipeForm(forms.Form):
    @staticmethod
    def category_choices():
        categories = Categories.objects.all()
        choices_list = []
        for category in categories:
            res_tuple = (category.id, category.title)
            choices_list.append(res_tuple)
        return choices_list

    recipe_title = forms.CharField(label='Название', max_length=150, required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipe_category = forms.ChoiceField(label='Категория', choices=category_choices(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    recipe_description = forms.CharField(label='Краткое описание', max_length=800, required=False,
                                         widget=forms.Textarea(attrs={'class': 'form-control'}))
    recipe_steps = forms.CharField(label='Шаги приготовления', max_length=2000, required=False,
                                   widget=forms.Textarea(attrs={'class': 'form-control'}))
    recipe_cooking_time = forms.IntegerField(label='Время приготовления (в минутах)', min_value=1, required=False,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
