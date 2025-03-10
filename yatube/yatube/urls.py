"""yatube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from posts import views
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    import debug_toolbar

handler404 = "posts.views.page_not_found" # noqa
handler500 = "posts.views.server_error" # noqa

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("Users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("about/", include('django.contrib.flatpages.urls')),
    path("group/<slug:slug>/", views.group_posts, name="group_posts"),
    path("new/", views.new_post, name="new_post"),
    path("500/", views.server_error, name="server_error"),
    # path('sentry-debug/', trigger_error),
]

from django.contrib.flatpages import views

urlpatterns += [
    path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='tech'),
    path("", include("posts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
