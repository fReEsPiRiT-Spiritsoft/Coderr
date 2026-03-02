from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer
from .permissions import IsAdminUser, IsCustomerUser
from orders.models import Order
from django.db.models import Q
from rest_framework.generics import RetrieveUpdateAPIView
from .permissions import IsBusinessUserOfOrder
from rest_framework.generics import RetrieveUpdateDestroyAPIView


class OrderListCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        output_serializer = OrderSerializer(order)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class OrderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    GET  /api/orders/{id}/ -> any involved user (customer or business)
    PATCH /api/orders/{id}/ -> only business_user can update status
    """
    queryset = Order.objects.select_related('customer_user', 'business_user').all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusinessUserOfOrder]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return OrderUpdateSerializer
        return OrderSerializer
    


class OrderRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET  /api/orders/{id}/ -> any involved user (customer or business)
    PATCH /api/orders/{id}/ -> only business_user can update status
    DELETE /api/orders/{id}/ -> only admin/staff can delete (204 No Content)
    """
    queryset = Order.objects.select_related('customer_user', 'business_user').all()
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.request.method in ('PATCH', 'PUT'):
            return [IsAuthenticated(), IsBusinessUserOfOrder()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return OrderUpdateSerializer
        return OrderSerializer
    

class OrderCountAPIView(APIView):
    """
    GET /api/order-count/{business_user_id}/
    Returns count of in_progress orders for a specific business user.
    Auth required (TokenAuthentication).
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            count = Order.objects.filter(
                business_user_id=business_user_id,
                status='in_progress'
            ).count()
            return Response({'order_count': count}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {'detail': 'Business user not found.'},
                status=status.HTTP_404_NOT_FOUND
            )