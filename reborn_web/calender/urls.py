from django.urls import path
from . import views

app_name = 'calendar'

urlpatterns = [
	path('', views.calendar_view, name='calendar'),
	path('alleventsj/', views.allEventsJSON, name='allEventsJSON'),
	path('updateEvent/', views.updateEvent, name='updateEvent'),
	path('viewEvent/', views.viewEvent, name='viewEvent'),
	path('forceDelete/', views.forceDelete, name='forceDelete'),
	path('allEvents/', views.allEvents, name='allEvents'),
]