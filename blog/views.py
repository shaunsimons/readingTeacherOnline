from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.http import Http404

def allBlogs(request):
    blogs = Blog.objects.order_by('-created_on')
    newest = blogs[0]
    rest_of_blogs = blogs[1:]
    return render(request, "blog/all_blogs.html", {'newest': newest, 'rest_of_blogs': rest_of_blogs})


def detail(request, slug):
    blog_detail = get_object_or_404(Blog, slug=slug)
    if blog_detail.status == 1 or request.user.is_superuser:
        return render(request, 'blog/detail.html', {'blog':blog_detail})
    else:
        raise Http404('Blog does not exist')


def redirect_to_home(request):
    return redirect('home')

