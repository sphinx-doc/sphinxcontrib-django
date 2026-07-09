from django.http import HttpResponse


def simple_view(request):
    """A simple view function."""
    return HttpResponse("Hello")


def not_a_view():
    """A function which is not mapped to any URL."""
