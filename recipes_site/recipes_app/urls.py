from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_page, name='recipe_page'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('registration/', views.registration, name='registration'),
    path('upload_image/<int:recipe_id>', views.upload_image, name='upload_image'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('categories/', views.categories_view, name='categories'),
    path('category_recipes/<int:category_id>', views.category_recipes, name='category_recipes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)