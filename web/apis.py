from django.http import Http404, JsonResponse
from .utils import views_functions

def index_view_api(request):
    try:
        key = request.GET['key']
        if key == "who_region_new_cases":
            data = views_functions.who_region_new_cases()
            return JsonResponse({"success": True, "data": data})
        elif key == "case_ratio":
            data = views_functions.case_ratio()
            return JsonResponse({"success": True, "data": data})
        elif key == "summary":
            data = views_functions.world_summary()
            return JsonResponse({"success": True, "data": data})
        elif key == "continent":
             filter_type = request.GET['filter_type']
             data = views_functions.continent_cases(filter_type)
             return JsonResponse({"success": True, "data": data})
        elif key == "country_summary":
            data = views_functions.country_summary()
            return JsonResponse({"success": True, "data": data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


def vietnam_view_api(request):
    try:
        key = request.GET['key']
        if key == "daily_data":
            filter_type = request.GET['filter_type']
            cases, actives = views_functions.vietnam_daily()
            if filter_type == "cases":
                daily_data = cases
            else:
                daily_data = actives
            return JsonResponse({"success": True, "data": daily_data})
        elif key == "summary":
            data = views_functions.vietnam_summary()
            return JsonResponse({"success": True, "data": data})
        elif key == "age":
            data = views_functions.vietnam_age()
            return JsonResponse({"success": True, "data": data})
        elif key == "nationality":
            data = views_functions.vietnam_nationality()
            return JsonResponse({"success": True, "data": data})
        elif key == "city_summary":
            data = views_functions.cities_summary()
            return JsonResponse({"success": True, "data": data})
        elif key == "gender":
            data = views_functions .vietnam_gender()
            return JsonResponse({"success": True, "data": data})
        elif key == "city_geomap":
            data = views_functions.cities_geomap()
            return JsonResponse({"success": True, "data": data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
