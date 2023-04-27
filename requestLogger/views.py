from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import APIRequestLog
from .serializers import APIRequestLogSerializer

#Python Decorator
def requestLogger(func):
    def inner(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
            log = APIRequestLog(path=request.path, method=request.method, status_code=response.status_code)
            log.response_data = response.data
            log.save()
            # serializer = APIRequestLogSerializer(log)
        except Exception as e:
            log = APIRequestLog(path=request.path, method=request.method, status_code=500)
            log.save()
            raise e
        
        return response
    
    return inner


# Create your views here.
@api_view(['GET'])
@requestLogger
def testView(request):
    data = {'message': 'Hello, world!'}
    return Response(data)


def homeView(request):
    return HttpResponse('This is the home page')
