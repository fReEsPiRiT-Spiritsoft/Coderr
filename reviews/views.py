from django.http import JsonResponse


def review_list(request):
    return JsonResponse({'detail': 'reviews list - implement logic'}, status=200)


def review_detail(request, id):
    return JsonResponse({'detail': f'review {id} - implement logic'}, status=200)
