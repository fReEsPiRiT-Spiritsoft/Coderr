from django.http import JsonResponse


def order_list(request):
    return JsonResponse({'detail': 'orders list - implement logic'}, status=200)


def order_detail(request, id):
    return JsonResponse({'detail': f'order {id} - implement logic'}, status=200)


def order_count(request, business_user_id):
    return JsonResponse({'detail': f'order count for {business_user_id} - implement logic'}, status=200)


def completed_order_count(request, business_user_id):
    return JsonResponse({'detail': f'completed order count for {business_user_id} - implement logic'}, status=200)
