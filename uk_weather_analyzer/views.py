from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import models
import functions
import json


@csrf_exempt
def home(request):
    template = loader.get_template('uk_weather_analyzer/index.html')
    context = {
        'count': models.get_kudos(),
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def kudos(request):
    data = json.loads(request.body)
    # print data
    value = data['count']
    if value in [1]:
        models.add_kudos()

    return JsonResponse({'count': models.get_kudos()})


@csrf_exempt
def api_readings(request):
    # print data
    region = request.GET['region']
    mode = request.GET['mode']

    if models.Region.objects.filter(Name=region).exists() and models.Mode.objects.filter(Name=mode).exists() :
        region_obj = models.Region.objects.filter(Name=region)
        mode_obj = models.Mode.objects.filter(Name=mode)
        data = models.Readings.objects.filter(Mode=mode_obj[0], Region=region_obj[0]).order_by('Year')
        results = [ob.to_dict() for ob in data]
        return JsonResponse(dict(results=results))
    else:
        return JsonResponse({'updated': False})


@csrf_exempt
def api_modes(request):
    results = [ob.to_dict() for ob in models.Mode.objects.all()]
    return JsonResponse({'results': results})


@csrf_exempt
def api_regions(request):
    results = [ob.to_dict() for ob in models.Region.objects.all()]
    return JsonResponse({'results': results})


@csrf_exempt
def update(request):
    region = request.GET['region']
    mode = request.GET['mode']

    if models.Region.objects.filter(Name=region).exists() and models.Mode.objects.filter(Name=mode).exists() :
        region_obj = models.Region.objects.filter(Name=region)
        mode_obj = models.Mode.objects.filter(Name=mode)
        link_obj = models.Link.objects.filter(Mode=mode, Region=region)
        functions.get_and_save_readings(link_obj[0].Link, region_obj[0], mode_obj[0])
        return JsonResponse({'updated': True})
    else:
        return JsonResponse({'updated': False})


@csrf_exempt
def update_all(request):
    done = functions.get_updates()
    return JsonResponse({'updated': done})


@csrf_exempt
def delete(request):
    done = models.delete_everything_from_readings()
    return JsonResponse({'deleted_all': done})