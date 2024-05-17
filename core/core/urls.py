from django.contrib import admin
from django.urls import path, include
from events.admin import events_admin_site
from yachts.admin import yachts_admin_site

urlpatterns = [
    # Built-In Admin Routes
    path('admin/', admin.site.urls),
    path('eventsadmin/', events_admin_site.urls),
    path('yachtsadmin/', yachts_admin_site.urls),
    
    # application routes
    path('', include('events.urls', namespace='events')),
]