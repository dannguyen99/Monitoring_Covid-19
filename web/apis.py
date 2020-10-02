from django.http import Http404, JsonResponse
from .utils import views_functions


def index_view_api(request):
    try:
        key = request.GET['key']
        if key == "who_region_new_cases":
            data = views_functions.who_region_new_cases()
            return JsonResponse({"success": True, "data": data})
        elif key == "case_ratio":
            data = views_functions.case_ratio(request.GET['language'])
            return JsonResponse({"success": True, "data": data})
        elif key == "summary":
            data = views_functions.world_summary()
            return JsonResponse({"success": True, "data": data})
        elif key == "continent":
            filter_type = request.GET['filter_type']
            data = views_functions.continent_cases(
                filter_type, request.GET['language'])
            return JsonResponse({"success": True, "data": data})
        elif key == "country_summary":
            data = views_functions.country_summary()
            return JsonResponse({"success": True, "data": data})
        elif key == "timeline_data":
            filter_type = request.GET['filter_type']
            daily_data = views_functions.index_daily_cases_chart()
            if filter_type == 'cases':
                data = daily_data[:, [0, 1]].tolist()
            else:
                data = daily_data[:, [0, 2]].tolist()
            return JsonResponse({"success": True, "data": data})
        elif key == "change_world_map":
            filter_type = request.GET['filter_type']
            data = views_functions.change_world_map(filter_type)
            return JsonResponse({"success": True, "geochart_data": data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


def vietnam_view_api(request):
    try:
        key = request.GET['key']
        if key == "daily_data":
            data = views_functions.vietnam_daily()
            return JsonResponse({"success": True, "data": data})
        elif key == "summary":
            data = views_functions.vietnam_summary()
            return JsonResponse({"success": True, "data": data})
        elif key == "age":
            data = views_functions.vietnam_age()
            return JsonResponse({"success": True, "data": data})
        elif key == "nationality":
            if request.GET.get('language'):
                data = views_functions.vietnam_nationality(request.GET['language'])
            else:
                data = views_functions.vietnam_nationality()
            return JsonResponse({"success": True, "data": data})
        elif key == "city_summary":
            data = views_functions.cities_summary()
            return JsonResponse({"success": True, "data": data})
        elif key == "gender":
            if request.GET.get('option'):
                if request.GET['option'] == "header":
                    data = views_functions.vietnam_gender_with_header(
                        request.GET['language'])
                    return JsonResponse({"success": True, "data": data})
                elif request.GET['option'] == "timeline":
                    data = views_functions.vietnam_gender_timeline()
                    return JsonResponse({"success": True, "data": data})
            else:
                data = views_functions.vietnam_gender()
                return JsonResponse({"success": True, "data": data})
        elif key == "city_geomap":
            data = views_functions.cities_geomap()
            return JsonResponse({"success": True, "data": data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
