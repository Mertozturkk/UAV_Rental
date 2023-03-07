from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('customer_dashboard/', include('customer_dashboard.urls')),
    path('uav_dealer_dashboard/', include('uav_dealer_dashboard.urls')),
]
