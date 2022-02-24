from django.contrib import admin
from django.urls import path

from shortener import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_form),
    path('search', views.get_full_url),
    path('add', views.convert_url),
    path('<short_name>', views.redirect_to_full_url)
]
