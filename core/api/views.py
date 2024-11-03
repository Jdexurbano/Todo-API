from django.http import JsonResponse

def getRoutes(request):

    routes = [
        'api/',
    ]

    return JsonResponse(routes, safe=False)