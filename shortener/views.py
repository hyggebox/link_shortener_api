import string

from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string

from .forms import ShortenLinkForm
from .models import Link


def show_form(request):
    if request.method == 'POST':
        form = ShortenLinkForm(request.POST)
        if form.is_valid():
            users_string = form.cleaned_data.get('custom_name')
            full_url = form.cleaned_data.get('full_url')
            if not users_string:
                short_name = get_random_string(
                    5, allowed_chars=string.ascii_lowercase
                )
            else:
                short_name = users_string

            Link.objects.create(short_name=short_name,
                                full_url=full_url)
            current_site = Site.objects.get_current()
            return JsonResponse(
                {
                    'full_url': full_url,
                    'short_url': f'https://{current_site.domain}/{short_name}'
                },
                status=200)

    form = ShortenLinkForm()
    return render(request, 'index.html', context={'form': form})


def redirect_to_full_url(request, short_name):
    users_link = Link.objects.filter(short_name=short_name).first()
    if users_link:
        current_site = Site.objects.get_current()
        return HttpResponseRedirect(users_link.full_url)
    return JsonResponse(
        {
            'Error': 'No such short url in the database'
        },
        status=404
    )