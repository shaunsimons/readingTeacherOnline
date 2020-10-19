from django.shortcuts import render, get_object_or_404
from .models import Blog
from django.http import Http404

def allBlogs(request):
    blogs = Blog.objects.all()
    return render(request, "blog/all_blogs.html", {'blogs': blogs})


def detail(request, slug):
    blog_detail = get_object_or_404(Blog, slug=slug)
    if blog_detail.status == 1 or request.user.is_superuser:
        return render(request, 'blog/detail.html', {'blog':blog_detail})
    else:
        raise Http404('Blog does not exist')


