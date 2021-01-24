from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from memberships.models import Customer
from courses_site.models import Course, Video, Watched
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core import mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generator_token
from django.utils.html import strip_tags
from smtplib import SMTPException
from django.contrib import messages
from datetime import timedelta
from blog.models import Blog


def home(request):
    get_premium = True
    how_learn_to_read_blog = Blog.objects.get(slug='how-our-brains-learn-to-read')
    try:  # logged in and member
        if request.user.customer.current_period_end > timezone.now():
            get_premium = False
    except Customer.DoesNotExist:  # logged in and not member
        get_premium = True
    except AttributeError:  # not logged in
        get_premium = True
    return render(request, 'course_site/main.html', {'get_premium': get_premium, 'how_learn_to_read_blog':how_learn_to_read_blog})


def signupuser(request):
    if request.method == 'GET':
        request.session['next'] = request.GET.get('next')
        return render(request, 'auth/signupuser.html')
    elif request.method == 'POST':
        # username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password1']
        try:
            user = User.objects.create_user(username=email,  # username is email address
                                            first_name=firstname.capitalize(),
                                            last_name=lastname.capitalize(),
                                            email=email,
                                            password=password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Reading Teacher Online Account Activation'
            message = render_to_string('auth/account_activation.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': generator_token.make_token(user),
                                           'protocol': request.scheme
                                       })
            plain_message = strip_tags(message)
            from_email = settings.DEFAULT_FROM_EMAIL
            mail.send_mail(email_subject, plain_message, from_email, [email], html_message=message)
            return redirect('activation_email_sent')

        except IntegrityError:
            messages.error(request, 'Email address is already taken')
            return render(request,
                          'auth/signupuser.html',
                          {'email_is_invalid': 'is-invalid',
                           'firstname': firstname,
                           'lastname': lastname,
                           'email': email,
                           'make_valid': 'is-valid'})
        except SMTPException as e:
            user.delete()
            print(e)
            messages.error(request, 'An error occurred while creating your account. Please try again. ')
            return render(request,
                          'auth/signupuser.html',
                          {'firstname': firstname,
                           'lastname': lastname,
                           'email': email,
                           'make_valid': 'is-valid'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'auth/loginuser.html')
    else:
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Login Failed.')
            messages.error(request, 'Either you credentials are incorrect or you need to activate your account')
            return redirect('loginuser')
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
    video_order = course_details.get_video_order()
    course_videos = Video.objects.filter(pk__in=video_order).order_by('_order')
    total_duration_timedelta = course_videos.aggregate(Sum('length'))
    total_duration = course_length_formatter(total_duration_timedelta['length__sum'])
    number_of_lectures = len(course_videos)
    if course_details.status == 1 or request.user.is_superuser:
        return render(request,
                      'course_site/course_detail.html',
                      {
                          'course_detail': course_details,
                          'videos': course_videos,
                          'slug': slug,
                          'total_duration': total_duration,
                          'number_of_lectures': number_of_lectures
                      }
                      )
    else:
        raise Http404('Course does not exist')


def course_length_formatter(duration: timedelta):
    return_string = ''
    total = int(duration.total_seconds())

    hours = total // 3600
    if hours > 0:
        return_string += f'{hours} hours'

    minutes = total % 3600 // 60
    if minutes > 0:
        return_string += f' {minutes} minutes'
    return return_string


def course_video(request, slug, order_number):
    course_details = get_object_or_404(Course, slug=slug)
    video_order = course_details.get_video_order()
    course_videos = Video.objects.filter(pk__in=video_order).order_by('_order')
    total_duration_timedelta = course_videos.aggregate(Sum('length'))
    total_duration = course_length_formatter(total_duration_timedelta['length__sum'])
    number_of_lectures = len(course_videos)
    if course_details.status == 1 or request.user.is_superuser:
        try:
            selected_video = video_order[order_number-1]
        except IndexError:
            raise Http404(f'There is no video {order_number} in {course_details.title}')
        video = get_object_or_404(Video, id=selected_video)


        if order_number == 0:
            previous_video = False
            next_video = 1
        elif order_number == len(video_order):
            previous_video = len(video_order) - 1
            next_video = False
        else:
            previous_video = order_number - 1
            next_video = order_number + 1

        if video.free_to_watch:
            return render(request, 'course_site/video.html',
                          {'video': video,
                           'course_details': course_details,
                           'current_number': order_number,
                           'previous': previous_video,
                           'next': next_video,
                           'slug': slug,
                           'all_videos': course_videos,
                           'total_duration': total_duration,
                           'number_of_lectures': number_of_lectures
                           })
        try:
            if request.user.is_superuser or request.user.customer.current_period_end > timezone.now():
                return render(request, 'course_site/video.html',
                              {'video': video,
                               'course_details': course_details,
                               'current_number': order_number,
                               'previous': previous_video,
                               'next': next_video,
                               'slug': slug,
                               'all_videos': course_videos,
                               'total_duration': total_duration,
                               'number_of_lectures': number_of_lectures
                               })
            else:
                redirect('memberships:join')
        except Customer.DoesNotExist:
            return redirect('memberships:join')
        except AttributeError:
            return redirect('loginuser')
    else:
        raise Http404('Course does not exist')


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user is not None and generator_token.check_token(user, token=token):
        user.is_active = True
        user.save()
        return redirect('account_activation_complete')
    return render(request, 'auth/activate_failed.html', {'support_email': settings.DEFAULT_FROM_EMAIL}, status=401)


def activation_email_sent(request):
    return render(request, 'auth/activation_email_sent.html')


def account_activated(request):
    return render(request, 'auth/account_activation_complete.html')


def error_404(request, exception):
    return render(request, '404.html')

def error_500(request, exception):
    return render(request, '500.html')