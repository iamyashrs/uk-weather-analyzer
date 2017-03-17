from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home),
    url(r'^kudos', views.kudos),
    url(r'^update/', views.update),
    url(r'^update_all/', views.update_all),
    # url(r'^blog/', include('blog.urls')),
    url(r'^_ah/', include('djangae.urls')),
    # url(r'^cron/', include(admin.site.urls)),

    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),

    url(r'^auth/', include('djangae.contrib.gauth.urls')),

    url(r'^api/readings/$', views.api_readings),
    url(r'^api/modes/$', views.api_modes),
    url(r'^api/regions/$', views.api_regions),
]

urlpatterns += staticfiles_urlpatterns()
