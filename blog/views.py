from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, AboutMe
from django.http import Http404
import re


def allBlogs(request):
    blogs = Blog.objects.order_by('-created_on')
    about_me = AboutMe.objects.all()[0]
    try:
        newest = blogs[0]
        rest_of_blogs = blogs[1:]
        return render(request, "blog/all_blogs.html", {'newest': newest, 'rest_of_blogs': rest_of_blogs, "about_me": about_me})
    except IndexError:
        return render(request, "blog/no_blogs.html", {"about_me": about_me})


def detail(request, slug):
    blog_detail = get_object_or_404(Blog, slug=slug)
    about_me = AboutMe.objects.all()[0]
    if blog_detail.status == 1 or request.user.is_superuser:
        return render(request, 'blog/detail.html', {'blog': blog_detail, "about_me": about_me})
    else:
        raise Http404('Blog does not exist')


def redirect_to_home(request):
    return redirect('home')

