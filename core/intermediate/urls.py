from django.urls import path
from . import views


app_name='intermediate'

urlpatterns = [
    #Working Patterns 
    path('', views.Index.as_view(), name="index"),
    path('intermediate/', views.IntermediateListView.as_view(), name='intermediate'),
    path('intermediate/<int:object2_id>/update/', views.EventRaceUpdateView.as_view(), name='update_intermediate'),   
    
    path('submitview/', views.submit_view),
    path('formsetsubmitview/', views.formset_submit_view),
    path('formsetsubmitcbview/', views.ItemUpdateView.as_view(), name='formsetview'),

    path('event_race/<int:race_id>/update/', views.EventRaceUpdateView.as_view(), name='update_event_race_results'),  
    #Test Patterns
    path('event_race/<int:race_id>/results/', views.EventRaceResultsListView.as_view(), name='list_event_race_results'),  
]