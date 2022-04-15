from rest_framework import serializers, generics

from app.models import Location, LocationDetails, Parameter, ParameterValues


class ParameterValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterValues
        fields = ['id', 'value']


class ParameterSerializer(serializers.ModelSerializer):
    location = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='location-detail'
    )
    values = ParameterValuesSerializer(many=True, read_only=True)
    aggregation = serializers.StringRelatedField(source='get_aggregation')

    class Meta:
        model = Parameter
        fields = ['id', 'name', 'location', 'values', 'aggregation', 'measurements']


class LocationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDetails
        fields = ['id', 'city_name', 'country_code', 'timezone', 'state_code', 'lat', 'lon']


class LocationSerializer(serializers.ModelSerializer):
    # parameters = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     view_name='location-parameters',
    #     read_only=True
    # )
    # parameters = ParameterSerializer(many=True)
    parameters = serializers.StringRelatedField(many=True)
    aggregations = serializers.StringRelatedField(source='get_aggregations')
    details = LocationDetailsSerializer(many=True)

    class Meta:
        model = Location
        fields = ['id', 'description', 'parameters', 'aggregations', 'details']
