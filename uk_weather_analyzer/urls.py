from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', 'uk_weather_analyzer.views.home', name='home'),
    url(r'^kudos', 'uk_weather_analyzer.views.kudos', name='kudos'),
    url(r'^update/', 'uk_weather_analyzer.views.update', name='update'),
    url(r'^update_all/', 'uk_weather_analyzer.views.update_all', name='update_all'),
    url(r'^delete/', 'uk_weather_analyzer.views.delete', name='delete'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^_ah/', include('djangae.urls')),
    # url(r'^cron/', include(admin.site.urls)),

    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),

    url(r'^auth/', include('djangae.contrib.gauth.urls')),

    url(r'^api/readings/$', 'uk_weather_analyzer.views.api_readings', name='api_readings'),
    url(r'^api/modes/$', 'uk_weather_analyzer.views.api_modes', name='api_modes'),
    url(r'^api/regions/$', 'uk_weather_analyzer.views.api_regions', name='api_regions'),
]

urlpatterns += staticfiles_urlpatterns()


