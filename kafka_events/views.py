from django.http import HttpResponse
from django_grip import set_hold_stream

def events(request, topic):
	set_hold_stream(request, topic)
	return HttpResponse(content_type='text/event-stream')
