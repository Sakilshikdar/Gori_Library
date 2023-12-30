from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .import forms
from .import models
from .models import Post
from django.views.generic import CreateView, DeleteView, DetailView
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.generic import ListView


# @login_required
# def add_post(request):
#     if request.method == "POST":
#         post_form = forms.PostForm(request.POST)
#         if post_form.is_valid():
#             # post_form.cleaned_data['author'] = request.user
#             post_form.instance.author = request.user
#             post_form.save()
#             return redirect('homepage')
#     else:
#         post_form = forms.PostForm()
#     return render(request, 'add_post.html', {'data': post_form})


@method_decorator(login_required, name='dispatch')
class addPostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# @login_required
# def edit_post(request, id):
#     post = models.Post.objects.get(pk=id)
#     post_form = forms.PostForm(instance=post)
#     if request.method == "POST":
#         post_form = forms.PostForm(request.POST, instance=post)
#         if post_form.is_valid():
#             post_form.save()
#             return redirect('homepage')
#     return render(request, 'add_post.html', {'data': post_form})


# @method_decorator(login_required, name='dispatch')
# class EditPostView(UpdateView):
#     model = models.Post
#     form_class = forms.PostForm
#     template_name = 'profile.html'
#     pk_url_kwarg = 'id'
#     success_url = reverse_lazy('profile')


# @login_required
# def delete_post(request, id):
#     post = models.Post.objects.get(pk=id, author=request.user)
#     return redirect('profile')


# @method_decorator(login_required, name='dispatch')
# class DeletePostView(DeleteView):
#     model = models.Post
#     template_name = 'delete.html'
#     pk_url_kwarg = 'id'
#     success_url = reverse_lazy('profile')


class PostDetailsView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object  # post model er object ekhane store korlam
        print(post)
        comments = post.comments.all()
        comment_form = forms.CommentForm()

        context['comments'] = comments
        context['comment_form'] = comment_form
        return context


# @login_required
# def buy_car(request, id):
#     car = get_object(Post, pk=id)
#     print(car)
#     if car.quantity > 0:
#         Order.objects.create(user=request.user, car=car,
#                              quantity=1, total_price=car.price)
#         car.quantity -= 1
#         car.save()
#     return redirect('car_detail', car_id=car_id)


# class profile2(DetailView):
#     model = models.Post.objects.all()
#     print(model)
#     pk_url_kwarg = 'id'
#     template_name = 'profile.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         car = self.object  # post model er object ekhane store korlam
#         car['quantity'] - 1
#         cardata = car.cardata.all()
#         context['data'] = cardata
#         context['type'] = 'profile'
#         return context
