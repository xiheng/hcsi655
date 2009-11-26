from django.db import models
import datetime

# Create your models here.
class Person(models.Model):    
    screen_name = models.CharField(max_length =128, unique=True)
    deviceid = models.CharField(max_length =64, unique=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.screen_name, self.deviceid)

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    orientation = models.FloatField()
    
    def __unicode__(self):
        return u'%s %s %s %s' % (self.latitude, self.longitude, self.altitude, self.orientation)
    
    class Meta:
        unique_together = (("latitude", "longitude", "altitude", "orientation"))
    
    
class PixelColor(models.Model):
    location = models.ForeignKey(Location)
    pixel_col = models.TextField()
    uploaded_at = models.DateTimeField('uploaded at', auto_now_add=True)
    person = models.ForeignKey(Person)
    tags = models.TextField(null = True, blank = True)
