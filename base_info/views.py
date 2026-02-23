from django.http import JsonResponse


def base_info(request):
    return JsonResponse({'detail': 'base info - implement aggregation logic'}, status=200)
