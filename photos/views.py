from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import PostForm, UserForm, ComentForm
from .models import Post, Coment, Mask
import make_mask
import os
import cv2

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'bmp']



def create_post(request):
    if not request.user.is_authenticated():
        return render(request, 'photos/login.html')
    else:
        maskis = Mask.objects.all()
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.photo = request.FILES['photo']
            file_type = post.photo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'post': post,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'photos/create_post.html', context)
            post.save()
            for msk in maskis:
                make_mask.detect(post.photo.url)
            return render(request, 'photos/detail.html', {'post': post})
        context = {
            "form": form,
            'masks': maskis,
        }
        return render(request, 'photos/create_post.html', context)




def create_coment(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'photos/login.html')
    else:
        form = ComentForm(request.POST or None)
        post = get_object_or_404(Post, pk=post_id)
        coment = form.save(commit=False)
        if form.is_valid():
            coment = form.save(commit=False)
            coment.user = request.user
            coment.post = post
            coment.save()
            return render(request, 'photos/detail.html', {'post': post})
        context = {
            'post': post,
            "form": form,
            'coment' : coment,
        }
        return render(request, 'photos/create_coment.html', context)


def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    posts = Post.objects.filter(user=request.user)
    return render(request, 'photos/index.html', {'posts': posts})


def detail(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'photos/login.html')
    else:
        user = request.user
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'photos/detail.html', {'post': post, 'user': user})



def favorite_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    try:
        if post.is_favorite:
            post.is_favorite = False
        else:
            post.is_favorite = True
        post.save()
    except (KeyError, Post.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'photos/login.html')
    else:
        posts = Post.objects.filter(user = request.user)
        query = request.GET.get("q")
        if query:
            posts = posts.filter(
                Q(post_title__icontains=query)
            ).distinct()
            return render(request, 'photos/index.html', {
                'posts': posts,
            })
        else:
            return render(request, 'photos/index.html', {'posts': posts})

def index_all(request):
    if not request.user.is_authenticated():
        return render(request, 'photos/login.html')
    else:
        posts = Post.objects.all()
        query = request.GET.get("q")
        if query:
            posts = posts.filter(
                Q(post_title__icontains=query)
            ).distinct()
            return render(request, 'photos/index_all.html', {
                'posts': posts,
            })
        else:
            return render(request, 'photos/index_all.html', {'posts': posts})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'photos/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(user=request.user)
                return render(request, 'photos/index.html', {'posts': posts})
            else:
                return render(request, 'photos/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'photos/login.html', {'error_message': 'Invalid login'})
    return render(request, 'photos/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(user=request.user)
                return render(request, 'photos/index.html', {'posts': posts})
    context = {
        "form": form,
    }
    return render(request, 'photos/register.html', context)
