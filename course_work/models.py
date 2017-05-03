from django.db import models
from geoposition import Geoposition
from geoposition.fields import GeopositionField


class Driver(models.Model):
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=50)
    point = GeopositionField(default=Geoposition(55.7558, 37.6173))

    def __str__(self):
        return self.name

class Road(models.Model):
    start = models.ForeignKey('Location', related_name='fk_road_start')
    end = models.ForeignKey('Location', related_name='fk_road_end')
    time = models.IntegerField()

    def __str__(self):
        return '{},{},{}'.format(self.start, self.end, self.time)

class Passenger(models.Model):
    start = models.ForeignKey('Location', related_name='fk_passenger_start')
    end = models.ForeignKey('Location', related_name='fk_passenger_end')
    name = models.CharField(max_length=50)
    price = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return '{},{},{},{},{}'.format(self.start, self.end, self.name, self.price, self.date)
