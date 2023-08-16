from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView, SpectacularRedocView

urlpatterns = [
    path("dadmin/", admin.site.urls, name="djangoadmin"),
    path('rest/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("rest/v1/", include('apirest.urls')),
    path('rest/v1/schema/', SpectacularAPIView.as_view(), name='schema'),  # Asignar un nombre a la vista
    path('rest/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('rest/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    # # # path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
