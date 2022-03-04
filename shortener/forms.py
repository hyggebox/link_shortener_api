from django import forms
from django.core.validators import validate_slug


class ShortenLinkForm(forms.Form):
    full_url = forms.URLField(label='Ссылка*', required=True)
    custom_name = forms.CharField(label='Кастомное имя ссылки (по желанию)',
                                  validators=[validate_slug],
                                  required=False)
