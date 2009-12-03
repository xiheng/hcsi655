# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.utils import simplejson
from django.core.serializers import serialize
from graffity.sketch.twitter import Api
from graffity.sketch.models import Person, Location, PixelColor
import urllib2

#url example: http://127.0.0.1:8000/sketch/login?username=abcd&password=12345&deviceid=2123456 (parameters can be transfered by Post method)
def login(request):
    username = request.REQUEST["username"]
    password = request.REQUEST["password"]
    deviceid = request.REQUEST["deviceid"]
    
    api = Api(username = username, password = password)
    try: 
        messages = api.GetDirectMessages()
        #user = api.GetUser(username)
    except urllib2.HTTPError, e:
        if e.code == 401:
            return HttpResponse("Account does not exist in Twitter")
        else:
            return HttpResponse("Other problems")
    else:
        #check whether a user is existed
        #if yes, don't create the user in DB. Otherwise, create the user in the DB
        queryset = Person.objects.filter(screen_name = username)
        #print '%s , %s' % (person.name, person.screen_name)
        print len(queryset)
        if len(queryset) == 0:
            p = Person(screen_name = username, deviceid = deviceid)
            p.save()
            print 'no record'
        else:
            print 'record exists'
        
        #person = Person.objects.filter(screen_name = username)[0]    
        return HttpResponse("ok")

#url example w/o tags: http://127.0.0.1:8000/sketch/put/2123456?lat=12.222&long=22.4444&alt=33.4444&ori=11.444&pix=1,2,1312313:3,4,565464   (parameters can be transfered by Post method)
#url example with tags: http://127.0.0.1:8000/sketch/put/2123456?lat=12.222&long=22.4444&alt=33.4444&ori=11.444&pix=1,2,1312313:3,4,565464:&tags=dog,apple   (parameters can be transfered by Post method)        
def put(request, deviceid):
    latitude = request.REQUEST["lat"]
    longitude = request.REQUEST["long"]
    altitude = request.REQUEST["alt"]
    orientation = request.REQUEST["ori"]
    pix= request.REQUEST["pix"]
    tags= request.REQUEST.get("tags",None)

    #if the location info does not exist in DB, insert it to DB.
    queryset = Location.objects.filter(latitude = latitude, longitude = longitude, altitude = altitude, orientation = orientation)
    print len(queryset)
    if len(queryset) == 0:
        loc = Location(latitude = latitude, longitude = longitude, altitude = altitude, orientation = orientation)
        loc.save()
        print 'no record'
    else:
        print 'record exists'
    
    #get person instance by deviceid        
    location = Location.objects.filter(latitude = latitude, longitude = longitude, altitude = altitude, orientation = orientation)[0]
    queryset = Person.objects.filter(deviceid = deviceid)
    if len(queryset) == 0:
        print 'the user does not exist in DB'
        return HttpResponse("error")
    else:
        print 'user record exists'
        
    person = queryset[0]
    
    #insert pixelcolor info to DB        
    #if there is no tag info, insert pixelcolor info w/o tags. Otherwise, insert everything to DB
    if tags == None:
        pixelcol = PixelColor( location = location, pixel_col = pix, person = person)
        pixelcol.save()
    else:
        pixelcol = PixelColor( location = location, pixel_col = pix, person = person, tags = tags)
        pixelcol.save() 
        
    return HttpResponse("ok")

#provide location and deviceid
#url example: http://127.0.0.1:8000/sketch/get/2123456?lat=12.222&long=22.4444&alt=33.4444&ori=11.444 
def get(request, deviceid):
    latitude = request.REQUEST["lat"]
    longitude = request.REQUEST["long"]
    altitude = request.REQUEST["alt"]
    orientation = request.REQUEST["ori"]
    
    #if the location info does not exist in DB, return empty result. Otherwise, extract pixelcolors from DB
    queryset = Location.objects.filter(latitude = latitude, longitude = longitude, altitude = altitude, orientation = orientation)
    print len(queryset)
    if len(queryset) == 0:        
        print 'no result'
        return HttpResponse("no sketch data because there is no location info")
    else:
        print 'location info exists'
        l = queryset[0]
        pixelcols = PixelColor.objects.filter(location = l)
        json = serialize('json', pixelcols)
        return HttpResponse(json, mimetype = 'application/json')
    