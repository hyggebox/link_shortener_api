from django import forms
from django.core.validators import validate_slug, URLValidator


class ShortenLinkForm(forms.Form):
    full_url = forms.CharField(label='Ссылка, которую нужно сократить',
                                required=True,
                                validators=[URLValidator()])
    custom_name = forms.CharField(label='Кастомное имя ссылки (по желанию)',
                                  validators=[validate_slug],
                                  required=False)
