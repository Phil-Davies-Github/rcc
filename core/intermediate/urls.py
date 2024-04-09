from django.urls import path
from . import views


app_name='intermediate'

urlpatterns = [
    #Working Patterns 
    path('', views.Index.as_view(), name="index"),
    path('intermediate/', views.IntermediateListView.as_view(), name='intermediate'),
    path('intermediate/<int:object2_id>/update/', views.IntermediateUpdateView.as_view(), name='update_intermediate'),   
]