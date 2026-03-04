from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('offers/', views.offer_list, name='offers-list'),
    path('offers/<int:id>/', views.offer_detail, name='offers-detail'),
    path('offerdetails/<int:id>/', views.offer_details, name='offers-details-extended'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
