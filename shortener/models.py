from django.db import models


class LinkQuerySet(models.QuerySet):

    def name_taken(self, short_name):
        return self.filter(pk=short_name).exists()


class Link(models.Model):
    short_name = models.CharField(verbose_name='Короткое имя',
                                  max_length=100,
                                  primary_key=True)
    full_url = models.URLField(verbose_name='Полная ссылка', max_length=200)
    created_at = models.DateTimeField(verbose_name='Когда ссылка сокращена',
                                      auto_now_add=True, null=True)

    objects = LinkQuerySet.as_manager()

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Ссылку'
        verbose_name_plural = 'Ссылки'