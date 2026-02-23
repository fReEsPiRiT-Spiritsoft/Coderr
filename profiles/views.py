from django.http import JsonResponse


def profile_detail(request, pk):
    return JsonResponse({'detail': f'profile {pk} - implement logic'}, status=200)


def business_profiles(request):
    return JsonResponse({'detail': 'business profiles - implement logic'}, status=200)


def customer_profiles(request):
    return JsonResponse({'detail': 'customer profiles - implement logic'}, status=200)
