from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'j0shua.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^hymns/', include('hymns.urls', namespace="hymns")),

    url(r'^admin/', include(admin.site.urls)),
)

# Warning! Just use during development! Remove this for production use.
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
