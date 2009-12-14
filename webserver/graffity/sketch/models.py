from django.db import models
import datetime

from django.utils import simplejson

json_dumps = simplejson.dumps
json_loads = simplejson.loads


class Person(models.Model):
    screen_name=models.CharField(max_length=128, unique=True)
    deviceid=models.CharField(max_length=64, unique=True)
    created_at=models.DateTimeField('created at', auto_now_add=True)

    def __unicode__(self):
        return u'%s %s' % (self.screen_name, self.deviceid)


class Location(models.Model):
    latitude=models.FloatField()
    longitude=models.FloatField()
    altitude=models.FloatField(default=100) # going to fake this right now -jk-

    def __unicode__(self):
        return u'%f %f %f ' % (
            self.latitude,
            self.longitude,
            self.altitude, )


    def to_d(self):
        return {
            'la': self.latitude,
            'lo': self.longitude,
            }

    class Meta:
        unique_together=(("latitude", "longitude", "altitude",))


# a stroke represents a part of a drawing at any location.  the coordinates of
# the strokes will take into account the orientation since we treat any sketch
# as a cylindrical canvas. a grouping of strokes by creator and location will
# be considered a "sketch"
class Stroke(models.Model):
    creator = models.ForeignKey(Person)
    created_at=models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location)
    color = models.CharField(max_length=9) # just store them like #AABBCCFF
    points = models.TextField() # store a list as json: [[x0,y0],[x1,y1]]

    def to_d(self, detailed=False):
        # return dict of a Stroke, optimized for json
        # keys are: "c":color  "p":points
        d = {
            'c': self.color,
            'p': json_loads(self.points), # non-optimal but we want a list
            }
        if detailed:
            d.update(self.location.to_d())
            d['creator'] = self.creator.screen_name
            d['ts'] = str(self.created_at)
        return d

    @classmethod
    def get_near(self, lat, lon):
        # stick with me, we're going to kludge this for performance reasons.
        # we could calculate the spherical distance using euclid's
        # approximation but that end up being a giant ball of suck if we have
        # tons of paths
        # since 1 degree of latitude ~ 111 km
        # we can say that .01 deg of latitude ~ 1 km
        # for this reason, we're just going to pull every stroke +- .01 of the
        # desired location and that should give us strokes within ~1km
        # for longitude, we have to do a bit more since they are wider at the
        # equator and shrink as they approach the poles.
        # to overcome this, we'll use the following:
        #   d=111km (distance at equator for 1 degree)
        #   LonDist = d * (1 - (lat/90))
        #   LonBounds = lon +- (1/LonDist)
        # which will provide an approximation of degree distance by diminishing
        # the distance 1 degree represents the further the lat gets from teh
        # equator.  Again, I stress this is an optimization for speed and I
        # wouldn't navigate ships by this :) -jk-

        lat_min = lat - abs(lat * .10)
        lat_max = lat + abs(lat * .10)

        lon_dist = 111.0 * (1-(lat/90.0))
        lon_min = lon - abs(1/lon_dist)
        lon_max = lon + abs(1/lon_dist)

        return Stroke.objects.filter( 
            location__latitude__gte=lat_min,
            location__latitude__lte=lat_max,
            location__longitude__gte=lon_min,
            location__longitude__lte=lon_max
            )


# '{"sketch": {"lat": 30.589344000000001, "strokes": [{"c": "#ff000060", "p": [[52, 80], [80, 80]]}], "lon": -96.307632999999996}}'

def get_sketch(loc,creator=None):
    strokes = Stroke.objects.filter(location=loc)
    if creator: strokes = strokes.filter(creator=creator)
    sketch = {'lat':loc.latitude, 'lon':loc.longitude, 'strokes':[]}
    for s in strokes:
        sketch['strokes'].append(s.to_d())
    return s


