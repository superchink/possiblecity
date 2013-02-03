# philadelphia/urls.py

from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from possiblecity.philadelphia.views import *
 
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='philadelphia/public.html'), 
        name='lotxlot'),

	url(r'^api/v1/lots/vacant/$', BoundingBoxVacantLotSearch.as_view(), name="api_lots_vacant"),

    url(r'^lots/vacant/$', TemplateView.as_view(template_name='philadelphia/vacant.html'), 
        name='lots_vacant'),

    url(r'^locate/$', TemplateView.as_view(template_name='philadelphia/locate.html'), 
        name='locate'),

    url(r'^search/$', LotsNearAddress.as_view(), name='search'),

	url(r'^lot/(?P<pk>\d+)/$', LotDetailView.as_view(), name='lot_detail'),

    url(r'^geo/lots/lot/(?P<pk>\d+)/$', LotDetailMapView.as_view(), name='geo_lot_detail'),  
  
    url(r'^vacant/available/$', cache_page(AvailableVacantLotListView.as_view(),60*60), 
        name='available_lots'),
    
)
