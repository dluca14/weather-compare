# from rest_framework import viewsets, generics
# from rest_framework import permissions
# from rest_framework.response import Response
# from django.http import HttpResponse, JsonResponse
#
# from app.models import Location, Parameter, LocationDetails
# from app.serializers import LocationSerializer, LocationDetailsSerializer, ParameterSerializer
#
#
# class LocationViewSet(viewsets.ModelViewSet):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer
#     # permission_classes = [permissions.IsAuthenticated]
#
#     # def retrieve(self, request, *args, **kwargs):
#     #     instance = self.get_object().details.all()[0]
#     #     serializer = LocationDetailsSerializer(instance)
#     #     from rest_framework.renderers import JSONRenderer
#     #
#     #     return Response({
#     #         'name': 'anme',
#     #         'sdnka': 'fmak'
#     #     })
#
#     @action(detail=True)
#     def group_names(self, request, pk=None):
#         """
#         Returns a list of all the group names that the given
#         user belongs to.
#         """
#         user = self.get_object()
#         groups = user.groups.all()
#         return Response([group.name for group in groups])
#
#
# class LocationDetailsViewSet(viewsets.ModelViewSet):
#     queryset = LocationDetails.objects.all()
#     serializer_class = LocationDetailsSerializer
#     # permission_classes = [permissions.IsAuthenticated]
#
#
# class ParameterViewSet(viewsets.ModelViewSet):
#     queryset = Parameter.objects.all()
#     serializer_class = ParameterSerializer
#     # permission_classes = [permissions.IsAuthenticated]
#
#
# # class ParameterDetail(generics.RetrieveUpdateDestroyAPIView):
# #     # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
# #
# #     queryset = Parameter.objects.all()
# #     serializer_class = ParameterSerializer


from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

from app.models import Location, Parameter, LocationDetails
from app.serializers import LocationSerializer, ParameterSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# class LocationDetailsViewSet(viewsets.ModelViewSet):
#     queryset = LocationDetails.objects.all()
#     serializer_class = LocationDetailsSerializer
#     # permission_classes = [permissions.IsAuthenticated]


class ParameterViewSet(viewsets.ModelViewSet):
    queryset = Parameter.objects.all().select_related(
        'location'
    )
    # .prefetch_related(
    #     'values'
    # )
    serializer_class = ParameterSerializer

    def get_queryset(self, *args, **kwargs):
        location_id = self.kwargs.get("location_pk")
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            raise NotFound('A location with this id does not exist')
        return self.queryset.filter(location=location)

    def perform_create(self, serializer):
        serializer.save(location=self.request.location)


# class ParameterDetail(generics.RetrieveUpdateDestroyAPIView):
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#     queryset = Parameter.objects.all()
#     serializer_class = ParameterSerializer
