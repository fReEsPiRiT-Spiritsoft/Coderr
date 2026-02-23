from django.http import JsonResponse


def offer_list(request):
    return JsonResponse({'detail': 'offers list - implement logic'}, status=200)


def offer_detail(request, id):
    return JsonResponse({'detail': f'offer {id} - implement logic'}, status=200)


def offer_details(request, id):
    return JsonResponse({'detail': f'offer details {id} - implement logic'}, status=200)
