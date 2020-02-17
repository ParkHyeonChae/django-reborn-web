from django.urls import path
from . import views

app_name = 'calender'

urlpatterns = [
	path('', views.calender_view, name='calender'),
	path('alleventsj/', views.allEventsJSON, name='allEventsJSON'),
	path('updateEvent/', views.updateEvent, name='updateEvent'),
	path('viewEvent/', views.viewEvent, name='viewEvent'),
	path('forceDelete/', views.forceDelete, name='forceDelete'),
	path('allEvents/', views.allEvents, name='allEvents'),
]