from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission, Group, GroupManager
from django.core.serializers import serialize
from django.http import  HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
# Create your views here.
from .models import Post, PostView, Like, Comment, User
from .forms import PostForm, CommentForm, UserRegisterForm, LoginForm
class PostListView(LoginRequiredMixin, ListView):
    model = Post

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def pos(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect('post:detail', slug=post.slug)
        return redirect('post:detail', slug=self.get_object().slug)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm() 
        return context
    

    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        PostView.objects.get_or_create(user=self.request.user, post=object)
        return object

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_type"] = 'Crear' 
        return context
    
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_type"] = 'Crear' 
        return context

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

@login_required
def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        like_qs[0].delete()
        return redirect('post:detail', slug=slug)
    Like.objects.create(user=request.user, post=post)
    return redirect('post:detail', slug=slug)


class UserRegisterView(FormView):
    template_name = 'user/registrarusuario.html'
    form_class = UserRegisterForm

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context['title'] = 'Crear Usuario'
        context["view_type"] = 'Crear'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario = User(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                nombres=form.cleaned_data.get('nombres'),
                apellidos=form.cleaned_data.get('apellidos'),
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()
            return redirect('post:list')


class LoginView(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('post:list')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        login(self.request, user)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('post:login'))