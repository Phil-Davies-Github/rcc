from django.urls import path
from . import views

app_name='intermediate'

urlpatterns = [
    # Home Route 
    path('', views.Index.as_view(), name="index"),
    # Events Routes
    path('year/', views.YearsListView.as_view(), name='year'),
    #path('year/<int:year>/events', views.EventsListView.as_view(), name = 'events'),
    path('year/<int:year>/events/', views.EventsListView.as_view(), name = 'events'),
    path('year/<int:year>/event/<int:event>/entries/', views.EventEntryListView.as_view(), name='event_entries'),
    
    # Results Routes
    path('event_race/<int:race_id>/update/', views.EventRaceUpdateView.as_view(), name='update_event_race_results'),  
    path('event_race/<int:race_id>/results/', views.EventRaceResultsListView.as_view(), name='list_event_race_results'),  
    path('event/<int:event_id>/results/', views.EventResultsListView.as_view(), name='list_event_results'), 

    # API Endpoints 
    path('api/years/', views.YearListAPIView.as_view(), name = 'api-years'),
    path('api/years/<int:year>/events/', views.YearEventListAPIView.as_view(), name = 'api-year-events'),
]