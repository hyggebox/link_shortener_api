import string

from django.core.validators import URLValidator, validate_slug
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from .forms import ShortenLinkForm
from .models import Link


def convert_url(full_url, users_string, hostname):
    short_name = users_string or create_short_name()
    Link.objects.create(short_name=short_name, full_url=full_url)
    return {'full_url': full_url,
            'short_url': f'http://{hostname}/{short_name}'}


def is_name_taken(short_name):
    return Link.objects.name_taken(short_name)


def create_short_name():
    char_num = 5
    generated_name = get_random_string(char_num,
                                       allowed_chars=string.ascii_lowercase)
    if is_name_taken(generated_name):
        return create_short_name()
    return generated_name


def show_form(request):
    if request.method == 'POST':
        form = ShortenLinkForm(request.POST)
        if not form.is_valid():
            return render(request, 'index.html',
                          context={'form': ShortenLinkForm(request.POST)})
        users_string = form.cleaned_data.get('custom_name')
        full_url = form.cleaned_data.get('full_url')
        if is_name_taken(users_string):
            return JsonResponse(
                {'Error': f'Short name `{users_string}` is already taken'},
                status=400)
        return JsonResponse(
            convert_url(full_url, users_string, request.get_host()),
            status=201
        )
    return render(request, 'index.html', context={'form': ShortenLinkForm()})


def redirect_to_full_url(request, short_name):
    users_link = Link.objects.filter(short_name=short_name).first()
    if users_link:
        return HttpResponseRedirect(users_link.full_url)
    return JsonResponse({'Error': 'No such short url in the database'},
                        status=404)


def get_full_url(request):
    short_name = request.GET.get('short_name', None)
    if not short_name:
        return JsonResponse({'Error': 'No params provided'}, status=400)
    users_link = Link.objects.filter(short_name=short_name).first()
    if users_link:
        return JsonResponse(
            {
                'full_url': users_link.full_url,
                'short_url': f'http://{request.get_host()}/{short_name}'
            },
            status=200)
    return JsonResponse({'Error': 'No such short url in the database'},
                        status=404)


@csrf_exempt
def create_short_url(request):
    url_to_convert = request.POST.get('url', '')
    users_string = request.POST.get('short_name', '')
    validate_url = URLValidator()
    try:
        validate_url(url_to_convert)
        try:
            validate_slug(users_string)
        except ValidationError:
            return JsonResponse(
                {'Error': 'short_name must consist of letters, numbers, '
                          'underscores or hyphens.'},
                status=400)
    except ValidationError:
        return JsonResponse({'Error': 'String is not valid URL'}, status=400)
    return JsonResponse(
        convert_url(url_to_convert, users_string, request.get_host()),
        status=200
    )
