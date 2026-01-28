from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'category', 'prep_time', 'cook_time', 'servings', 'difficulty', 'ingredients', 'instructions', 'image', 'is_public']
