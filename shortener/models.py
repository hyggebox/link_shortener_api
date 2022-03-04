from django.db import models


class Link(models.Model):
    short_name = models.CharField(verbose_name='Короткое имя',
                                  max_length=100,
                                  primary_key=True)
    full_url = models.URLField(verbose_name='Полная ссылка', max_length=200)

    def __str__(self):
        return f'{self.short_name}'

    class Meta:
        verbose_name = 'Ссылку'
        verbose_name_plural = 'Ссылки'