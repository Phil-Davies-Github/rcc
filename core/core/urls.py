from django.contrib import admin
from django.urls import path, include
from events.admin import events_admin
from yachts.admin import yachts_admin

admin.site.site_header = "RCC Admin"
admin.site.site_title = "RCC Admin Portal"
admin.site.index_title = "Welcome to RCC Portal"

urlpatterns = [
    # Built-In Admin Routes
    path('admin/', admin.site.urls),
    path('eventsadmin/', events_admin.urls),
    path('yachtsadmin/', yachts_admin.urls),
    
    # application routes
    path('', include('events.urls', namespace='events')),
]