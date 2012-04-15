# urls.py

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()

handler500 = "pinax.views.server_error"

urlpatterns = patterns('',
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r"^$", RedirectView.as_view(url="/blog"), {
        "template": "homepage.html",
    }, name="home"),

    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),

    # blog
    (r'^blog/', include('blog.urls')),


    # search
    (r'^search/', include('haystack.urls')),

)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )