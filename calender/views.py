from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
import json
from .models import Calender
from users.decorators import login_message_required, admin_required


# 학사일정
@login_message_required
def calendar_view(request):
	return render(request, 'calendar/calendar.html')


# 일정추가, 수정
@admin_required
def updateEvent(request):
	event_id = request.GET['eventId']
	event_name = request.GET['eventName']
	location = request.GET['eventLocation']
	start_date = request.GET['eventStartDate']
	end_date = request.GET['eventEndDate']
	all_day = request.GET['eventAllDay']
	description = request.GET['eventDescription']
	flag = 0
	id_start = 1

	if event_id == "":
		while flag == 0:
			if Calender.objects.filter(event_id = (str(id_start) + "-eve-" + start_date)).count() == 1:
				id_start += 1
			else:
				new_event_id = str(id_start) + "-eve-" + start_date
				flag = 1
		q = Calender(event_id = new_event_id, event_name = event_name, location = location, start_date = start_date, end_date = end_date, all_day = all_day, description = description)
		try:
			q.save()
			result = "Saved Successfully"
		except Exception as e:
			result = e
	else:
		new_event_id = event_id
		try:
			Calender.objects.filter(event_id = event_id).update(event_name = event_name, location = location, start_date = start_date, end_date = end_date, all_day = all_day, description = description, updated = (timezone.now() +timezone.timedelta(minutes=330)))
			result = "Event Updated"
		except Exception as e:
			result = e
	return HttpResponse(json.dumps({"result": result, "event_id": new_event_id}), content_type = "application/json")


# 일정표시
def allEvents(request):
	response = ""
	q = Calender.objects.filter(deleted = False).values()
	for x in range(0,q.count()):
		response += q[x]["event_id"] + "/" + q[x]["end_date"] + "/" + q[x]["event_name"] + ";"
	return HttpResponse(response)


# 일정 json응답
def allEventsJSON(request):
	response = {}
	q = Calender.objects.values()
	for x in range(0,q.count()):
		response[x] = {}
		response[x]["event_id"] = q[x]["event_id"]
		response[x]["event_google_id"] = q[x]["event_google_id"]
		response[x]["event_name"] = q[x]["event_name"]
		response[x]["location"] = q[x]["location"]
		response[x]["start_date"] = q[x]["start_date"]
		response[x]["end_date"] = q[x]["end_date"]
		response[x]["all_day"] = q[x]["all_day"]
		response[x]["description"] = q[x]["description"]
		response[x]["updated"] = str(q[x]["updated"])
		response[x]["deleted"] = q[x]["deleted"]
	return HttpResponse(json.dumps({"response": response}), content_type = "application/json")


# 세부일정보기
def viewEvent(request):
	event_id = request.GET['eventId']
	q = Calender.objects.get(event_id = event_id)
	return HttpResponse(json.dumps({"event_name": q.event_name, "location": q.location, "start_date": q.start_date, "end_date": q.end_date, "all_day": q.all_day, "description": q.description}), content_type = "application/json")


# 일정삭제
@admin_required
def forceDelete(request):
	event_id = request.GET['eventId']
	try:
		Calender.objects.filter(event_id = event_id).delete()
		result = "Deleted Successfully"
	except Exception as e:
		result = e
	return HttpResponse(json.dumps({"result": result, "event_id": event_id}), content_type = "application/json")

