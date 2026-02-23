from django.http import JsonResponse


def registration(request):
    return JsonResponse({'detail': 'registration endpoint - implement logic'}, status=200)


def login_view(request):
    return JsonResponse({'detail': 'login endpoint - implement logic'}, status=200)
