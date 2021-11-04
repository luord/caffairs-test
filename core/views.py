from asgiref.sync import sync_to_async
import json

from django.http import HttpResponse

from core.models import Application, Event


async def save_event(request):
    @sync_to_async
    def _check_application():
        return  Application.objects.filter(pk=request.headers.get('Application'), is_trusted=True).first()

    application = await _check_application()
    if not application:
        return HttpResponse('Application not trusted', status=403)

    @sync_to_async
    def _save():
        event = Event(**json.loads(request.body))
        event.save()
        return event

    event = await _save()
    await event.process()

    return HttpResponse('event saved', status=201)
