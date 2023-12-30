from django.shortcuts import render
from book.models import Post
from category.models import Category


def home(request, category_slug=None):
    data = Post.objects.all()
    if category_slug is not None:
        print('ok')
        category = Category.objects.get(slug=category_slug)
        data = Post.objects.filter(categorie=category)
    category2 = Category.objects.all()
    return render(request, 'home.html', {'data': data, 'category': category2})
