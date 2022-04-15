# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from app import views
#
# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# # router.register(r'parameters', views.ParameterViewSet, basename="parameter")
# router.register(r'locations', views.LocationViewSet, basename="location")
# # router.register(r'locations_details', views.LocationDetailsViewSet, basename="location_details")
#
# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
# ]


from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from app import views


router = SimpleRouter()
router.register('locations', views.LocationViewSet)

param_router = routers.NestedSimpleRouter(router, r'locations', lookup='location')
param_router.register(r'parameters', views.ParameterViewSet, basename='location-parameters')

# app_name = 'app'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(param_router.urls)),

    # re_path(r'^locations/(?P<location_id>\d+)/parameters/?$',
    #     views.ParameterViewSet.as_view({'get': 'list'}), name='location-parameters'),
    # re_path(r'^locations/(?P<location_id>\d+)/parameters/(?P<pk>\d+)/?$',
    #     views.ParameterViewSet.as_view({'get': 'retrieve'}), name='location-parameter-detail'),
]






