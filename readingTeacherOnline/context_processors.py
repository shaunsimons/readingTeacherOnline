
from courses_site.models import Course


def extras(request):
    courses = Course.objects.all()
    return {'courses': courses}
