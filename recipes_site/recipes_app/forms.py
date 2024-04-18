from django import forms

from .models import RecipeCategory


class RegistrationForm(forms.Form):
    user_name = forms.CharField(label='Your name', max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', max_length=150,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email Address',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password', max_length=100,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    user_name = forms.CharField(label='Your name', max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddRecipeForm(forms.Form):
    recipe_title = forms.CharField(label='Recipe title', max_length=150,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipe_category = forms.CharField(label='Recipe title', max_length=150,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipe_description = forms.CharField(label='Recipe description', max_length=800,
                                         widget=forms.Textarea(attrs={'class': 'form-control'}))
    recipe_steps = forms.CharField(label='Recipe steps', max_length=2000,
                                   widget=forms.Textarea(attrs={'class': 'form-control'}))
    recipe_cooking_time = forms.IntegerField(label='Recipe cooking time', min_value=1,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))


class UploadRecipeImageForm(forms.Form):
    image = forms.ImageField(label='Upload image', required=False)



class EditRecipeForm(forms.Form):
    recipe_title = forms.CharField(label='Recipe title', max_length=150,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipe_description = forms.CharField(label='Recipe description', max_length=800,
                                         widget=forms.Textarea(attrs={'class': 'form-control'}))
    recipe_steps = forms.CharField(label='Recipe steps', max_length=2000,
                                   widget=forms.Textarea(attrs={'class': 'form-control'}))
    recipe_cooking_time = forms.IntegerField(label='Recipe cooking time', min_value=1,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    recipe_photo = forms.ImageField(label='Recipe photo', required=False,
                                    widget=forms.FileInput(attrs={'class': 'form-control'}))
