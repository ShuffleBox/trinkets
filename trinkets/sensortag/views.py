from django.http import HttpResponse

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import renderers
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser



from serializers import SensorTagSerializer, SensorTagDetailSerializer, SensorDataSerializer
from models import SensorTag, SensorData

# required for human views
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext, Context

import ipdb

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class SensortagListReadView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get(self, request, format=None):
        sensortags = SensorTag.objects.all()
        serializer = SensorTagSerializer(sensortags, many=True)
        return Response(serializer.data)
    
class SensortagDetailReadUpdateView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get(self, request, mac_slug, year=None, month=None, day=None, format=None):
        sensortag = SensorTag.objects.get(slug = mac_slug)
        #ipdb.set_trace()
        if year and month and day:
            sensordata = sensortag.sensordata_set.filter(time_recorded__year = year).filter(time_recorded__month = month).filter(time_recorded__day = day)
        elif year and month:
            sensordata = sensortag.sensordata_set.filter(time_recorded__year = year).filter(time_recorded__month = month)
        elif year:
            sensordata = sensortag.sensordata_set.filter(time_recorded__year = year)
        else:
            sensordata = sensortag.sensordata_set.latest('time_recorded')
        
        if isinstance(sensordata, SensorData):
            serializer = SensorDataSerializer(sensordata)
        else:
            serializer = SensorDataSerializer(sensordata, many=True)

        return Response(serializer.data)
    
    def post(self, request, mac_slug, format=None):
        try:
            tag = SensorTag.objects.get(slug = mac_slug)
        except ObjectDoesNotExist:
       
            tag = SensorTag(mac_address=request.data['mac_address'], description='new tag')
            tag.save()
        
        #ipdb.set_trace()
        for key in ('lux', 'ambient_temp', 'humidity', 'ir_temp'):
            request.data[key] = unicode("%.2f" % (float(request.data[key])))
            
        serializer = SensorDataSerializer(data=request.data)
        
        #ipdb.set_trace()
        if serializer.is_valid():
            sensordata = SensorData(sensor=tag, **serializer.data)
            sensordata.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""
Human consumption views
"""

class SensorTagList(View):
    """
    List of SensorTags
    """
    template = 'sensortag_list.html'
    def get(self, request, *args, **kwargs):
        sensortags = SensorTag.objects.all()
        
        return render_to_response(self.template,
                                    {
                                    'title': 'TI SensorTag List',
                                    'sensortags': sensortags
                                    },
                                    context_instance=RequestContext(request)
                                )
    
    def post(self, request):
        return HttpResponse('POST here!')

class SensorTagDetail(View):
    """
    Detailed view of Sensortag
    Let's try to be ambitious and get graphing and updating of latest value in a table.
    """
    template = 'sensortag_detail.html'
    def get(self, request, *args, **kwargs):
        sensortag = get_object_or_404(SensorTag, slug=self.kwargs['sensortag'])
        # today = Datetime.now!
        # sensordataset = sensortag.sensordata_set.filter(time_recorded__day = day
        return render_to_response(self.template,
                                    {
                                    'title': 'TI SensorTag List',
                                    'sensortag': sensortag
                                    },
                                    context_instance=RequestContext(request)
                                )
    
    def post(self, request):
        return HttpResponse('POST here!')


            


