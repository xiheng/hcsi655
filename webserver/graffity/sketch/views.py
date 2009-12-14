# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.utils import simplejson
from django.core.serializers import serialize
from graffity.sketch.twitter import Api
from graffity.sketch.models import Person, Location, Stroke, get_sketch
import urllib2
from PIL import Image, ImageDraw

from re import match

json_dumps = simplejson.dumps
json_loads = simplejson.loads


def json_response(obj):
    return HttpResponse(json_dumps(obj))
    # return HttpResponse(json_dumps(obj), mimetype = 'application/json')


# convenience method to return a properly formatted success in json
def ok(extras=None):
    d = {'status':'ok'}
    if extras: d.update(extras)
    return json_response(d)


# convenience method to return a properly formatted failure in json
def fail(reason):
    return json_response({'status':'fail', 'reason':reason})


#url example:
# http://host/sketch/login?u=user&p=pass&d=2123456
def login(request):
    username = request.REQUEST["u"]
    password = request.REQUEST["p"]
    deviceid = request.REQUEST["d"]

    api = Api(username = username, password = password)
    try:
        # just do anything to check the connection
        messages = api.GetDirectMessages()
    except urllib2.HTTPError, e:
        if e.code == 401:
            return fail("Account does not exist in Twitter")
        else:
            return fail("Other problems")
    else:
        #does the user exist?  create if not
        p, _created = Person.objects.get_or_create(screen_name=username)
        if _created:
            p.deviceid = deviceid
            p.save()
        return ok()


# url: /put/DEVID?lat=12.22&lon=22.44&s=[[44,34],[80,33]]&c=aabbccdd
def put(request, deviceid):
    lat = float(request.REQUEST["lat"])
    lon = float(request.REQUEST["lon"])
    tags = request.REQUEST.get("tags",None)
    stroke_points = json_loads(request.REQUEST['s'])
    color = request.REQUEST['c']

    # check the color for proper format AABB8833
    if not match(r"[a-zA-Z0-9]{8}", color):
        return fail("bogus color")

    # check our stroke_points.  should be a list of tuples with 2 members each
    if type(stroke_points) not in (type(list()), type(tuple())):
        return fail("strokes not a list")

    # create location if doesn't exist
    loc,_created = Location.objects.get_or_create(
        latitude=lat,
        longitude=lon)
    if _created: loc.save()

    # get person instance by deviceid
    # XXX TODO -jk- this is sooo insecure as to be comical
    # XXX we should instead be assigning people a token when they auth
    # XXX and then make them continue using that throughout the session
    # try:
    #     person = Person.objects.get(deviceid = deviceid)
    # exist DoesNotExist:
    #     return HttpResponse("error")

    # we're just going to fake this for now.  XXX 
    person, _created = Person.objects.get_or_create(deviceid = deviceid)
    if _created:
        person.name = 'fake'
        person.save()

    # let's build a points list from the list they passed in.  it doubles up
    # the work but lets us do some sanity checking on the input
    points = []
    for (x,y) in stroke_points:
        # TODO we should tie the pixel size of the device's canvas in here and
        # calculate the x and y and make sure they're sane, but we're not going
        # to mess with it for now -jk-
        # TODO we could also do some optimization here, looking for overlapping
        # points, etc to actually minimize the storage, but that's a bit
        # tricky. You can't use a set instead of a list.  ORDER MATTERS -jk-
        points.append((x,y))
    
    Stroke(
        creator=person,
        location=loc,
        points=json_dumps(points),
        color=color
        ).save()

    return ok()


# returns strokes near a given location
# url: /strokes/LAT/LON/?c=CREATOR_NAME&dist=2.0
def strokes(request, lat, lon):
    lat=float(lat)
    lon=float(lon)
    creator = request.REQUEST.get('c')
    _s = Stroke.get_near(lat,lon)
    return ok({'sketch':[s.to_d(detailed=True) for s in _s]})


def map(request):
    #if the location info does not exist in DB, return empty result. Otherwise, extract pixelcolors from DB
    #queryset = Location.objects.filter(latitude = latitude, longitude = longitude, altitude = altitude, orientation = orientation)
    queryset = Location.objects.all()

    print len(queryset)
    if len(queryset) == 0:
        print 'no result'
        return HttpResponse("no sketch data because there is no location info")
    else:
        print 'location info exists'

        # create an empty set
        maparray = []
        for l in queryset:
            strokes = Stroke.objects.filter(location = l)
            #create image
            image = Image.new("RGB", (480, 320), "white")
            draw = ImageDraw.Draw(image)

            for stroke in strokes:
                #ToDo draw each pixel_col using draw.line and aggregate tags
                #draw.line([(52,80),(80,80)], fill = "black") #temporal usage
                stroke_points = json_loads(stroke.points)
                print stroke_points[0][0], stroke_points[0][1], stroke_points[1][0], stroke_points[1][1] 
                draw.line([(stroke_points[0][0],stroke_points[0][1]),(stroke_points[1][0],stroke_points[1][1])], fill = "#" + stroke.color) #temporal usage
                print l.latitude, l.longitude, l.altitude, stroke.color, stroke.points #stroke.tags
            imagename = str(l.latitude) + str(l.longitude) + str(l.altitude)#"image2"
            image.save( "media/" + imagename + ".bmp", "BMP")
            dic = dict([('lat',l.latitude), ('long', l.longitude), ('alt', l.altitude), ('image', "/sketch/media/" + imagename + ".bmp")])
            maparray.append(dic)

        #have to create image file
        return render_to_response('sketch/map.html', {'maparray': maparray})




