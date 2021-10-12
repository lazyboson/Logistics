from django.conf.urls import url
from serviceprovider import views


urlpatterns = [
    url(r'^serviceprovider/$', views.ProviderList.as_view(), name='ProviderList'),
    url(r'^serviceprovider/(?P<pk>.+)/$', views.ProviderDetail.as_view(), name='ProviderDetail'),
    url(r'^polygon/$', views.PolygonList.as_view(), name='PolygonList'),
    url(r'^polygon-details/(?P<pk>.+)/$', views.PolygonDetail.as_view(), name='PolygonDetail'),
    url(r'^get-lat-long-polygon-data/$', views.GetPolygonData.as_view(), name='PolygonData'),
]