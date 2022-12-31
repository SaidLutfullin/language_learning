from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dictionary.urls')),
    path('', include('authentication.urls')),
    path('', include('articles.urls')),
    path('', include('diary.urls')),
    path('', include('feedback.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "config.views.page_not_found_view"

if not settings.DEBUG:
    urlpatterns += re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
