from django.db import models


class Location(models.Model):
    description = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['id']

    def get_aggregations(self):
        aggregations = []
        for parameter in self.parameters.all():
            values_per_parameter = [v.value for v in parameter.values.all()]
            aggregations.append({
                'id': parameter.id,
                'name': parameter.name,
                'avg': sum(values_per_parameter)/len(values_per_parameter),
                'min': min(values_per_parameter),
                'max': max(values_per_parameter),
                'units': parameter.measurements
            })
        return aggregations


class LocationDetails(models.Model):
    location = models.ForeignKey(Location, related_name='details', on_delete=models.CASCADE)

    city_name = models.CharField(max_length=150)
    country_code = models.CharField(max_length=150)
    timezone = models.CharField(max_length=150)
    state_code = models.CharField(max_length=150)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return str({'city_name': self.city_name,
                    'timezone': self.timezone})


class Parameter(models.Model):
    location = models.ForeignKey(Location, related_name="parameters", on_delete=models.CASCADE)

    name = models.CharField(max_length=150)
    measurements = models.CharField(max_length=100, blank=True, default='')

    def get_aggregation(self):
        aggregation = {
            'id': self.id,
            'name': self.name,
            'avg': sum([pv.value for pv in self.values.all()]) / len([pv for pv in self.values.all()]),
            'min': min([pv.value for pv in self.values.all()]),
            'max': max([pv.value for pv in self.values.all()]),
            'units': self.measurements
        }
        return aggregation


class ParameterValues(models.Model):
    parameter = models.ForeignKey(Parameter, related_name='values', on_delete=models.CASCADE)

    value = models.FloatField()

    def __str__(self):
        return str(self.value)


# class LocationAggregations(models.Model):
#     name = models.CharField(max_length=150)
#     avg = models.FloatField()
#     min = models.FloatField()
#     max = models.FloatField()
#     units = models.CharField(max_length=150)
#
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location_aggregations')
#     parameter = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='parameter_aggregations')



# from app.models import Location, LocationDetails, Parameter, ParameterValues
# location = Location(description='Acasa')
# location.save()
# ldetails = LocationDetails(city_name="Timisoara", country_code="RO", timezone="UTC+2", lat=25.00, lon=44.00, location=location)
# ldetails.save()
# param1 = Parameter(name='Temperature', measurements='C', location=location)
# param1.save()
# param2 = Parameter(name='Precipitations', measurements='l/m2', location=location)
# param2.save()
# pvalue1 = ParameterValues(parameter=param1, value=25)
# pvalue1.save()
# pvalue2 = ParameterValues(parameter=param1, value=20)
# pvalue2.save()
# pvalue3 = ParameterValues(parameter=param1, value=27)
# pvalue3.save()
# pvalue4 = ParameterValues(parameter=param2, value=5)
# pvalue4.save()
# pvalue5 = ParameterValues(parameter=param2, value=10)
# pvalue5.save()
# pvalue6 = ParameterValues(parameter=param2, value=12)
# pvalue6.save()
