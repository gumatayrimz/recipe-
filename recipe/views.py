from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from .forms import RecipeForm


def recipe_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    # Show all public recipes + private recipes owned by the current user
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(models.Q(is_public=True) | models.Q(author=request.user))
    else:
        recipes = Recipe.objects.filter(is_public=True)

    if query:
        recipes = recipes.filter(name__icontains=query)
    if category:
        recipes = recipes.filter(category=category)

    categories = Recipe.CATEGORY_CHOICES

    return render(request, 'recipe/pages/recipe_list.html', {
        'recipes': recipes.distinct(),
        'query': query,
        'category': category,
        'categories': categories
    })


from django.urls import reverse

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {
        'recipe': recipe,
        'previous_url': request.META.get('HTTP_REFERER', reverse('recipe_list'))
    }
    return render(request, 'recipe/pages/recipe_detail.html', context)


from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Recipe created successfully!')
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    context = {
        'form': form,
        'previous_url': request.META.get('HTTP_REFERER', reverse('recipe_list'))
    }
    return render(request, 'recipe/pages/recipe_form.html', context)


@login_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Permission check
    if recipe.author != request.user:
        messages.error(request, "You don't have permission to edit this recipe.")
        return redirect('recipe_detail', pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_list')
    else:
        form = RecipeForm(instance=recipe)
    context = {
        'form': form,
        'recipe': recipe,
        'previous_url': request.META.get('HTTP_REFERER', reverse('recipe_list'))
    }
    return render(request, 'recipe/pages/recipe_form.html', context)


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Permission check
    if recipe.author != request.user:
        messages.error(request, "You don't have permission to delete this recipe.")
        return redirect('recipe_detail', pk=pk)

    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('recipe_list')
    return render(request, 'recipe/pages/recipe_confirm_delete.html', {'recipe': recipe})
