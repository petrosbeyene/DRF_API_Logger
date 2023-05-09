==================================================
Django Request-Response and Model Change Logger
==================================================

Django REST framework logger is an application to log requests/responses and model changes to the database.

Quick Start
==============
1. Install the package with the following command: pip install -i https://test.pypi.org/simple/ peter-sample-dfr-app
2. Add requestLogger to your project just like the following::
    INSTALLED_APPS = [
        ......
        "requestLogger"
    ]

3. import your requestLogger decorator in your views.py file and use it as follow:
#import your decorator
from requestLogger.views import requestLogger

#then you can use it at every api end point you have just like the example below,
@api_view(['GET'])
@requestLogger
def testView(request):
    data = {'message': 'Hello, world!'}
    return Response(data)
