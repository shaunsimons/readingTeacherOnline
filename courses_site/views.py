from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from memberships.models import Customer
from courses_site.models import Course, Video, Watched
from django.contrib.auth.decorators import login_required


def home(request):
    get_premium = True
    try:  # logged in and member
        if request.user.customer.current_period_end > timezone.now():
            get_premium = False
    except Customer.DoesNotExist:  # logged in and not member
        get_premium = True
    except AttributeError:  # not logged in
        get_premium = True
    return render(request, 'course_site/main.html', {'get_premium': get_premium})


def signupuser(request):
    if request.method == 'GET':
        request.session['next'] = request.GET.get('next')
        return render(request, 'course_site/signupuser.html')
    else:
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password1']
        try:
            user = User.objects.create_user(username=username,
                                            first_name=firstname,
                                            last_name=lastname,
                                            email=email,
                                            password=password)
            user.save()
            if request.POST.get('next') != '':
                login(request, user)
                return redirect(request.POST.get('next'))
            else:
                login(request, user)
                return redirect('home')
        except IntegrityError:
            return render(request,
                          'course_site/signupuser.html',
                          {'un_is_invalid': 'is-invalid',
                           'un_error_msg': 'Username is already taken.',
                           'firstname': firstname,
                           'lastname': lastname,
                           'email': email,
                           'username': username,
                           'make_valid': 'is-valid'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'course_site/loginuser.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'course_site/loginuser.html', {'error': 'Username and password did not match.'})
        else:
            if 'next' in request.POST:
                login(request, user)
                return redirect(request.POST.get('next'))
            else:
                login(request, user)
                return redirect('home')


def all_courses(request):
    courses = Course.objects.all()
    return render(request, 'course_site/all_courses.html', {'courses': courses})


def course_detail(request, slug):
    course_details = get_object_or_404(Course, slug=slug)
    course_videos = Video.objects.filter(course=course_details.id).values('order_number','title')

    return render(request, 'course_site/course_detail.html', {'course_detail': course_details, 'videos': course_videos})


@login_required(login_url='/login/')
def course_video(request, slug, order_number):
    course_details = get_object_or_404(Course, slug=slug)
    video = get_object_or_404(Video, course=course_details.id, order_number=order_number)
    if video.free_to_watch:
        return render(request, 'course_site/video.html', {'video': video})
    try:
        if request.user.customer.current_period_end > timezone.now():
            return render(request, 'course_site/video.html', {'video': video})
        else:
            redirect('memberships:join')

    except Customer.DoesNotExist:
        return redirect('memberships:join')

