from asgiref.sync import sync_to_async
import json

from django.http import HttpResponse

from core.models import Application, Event


async def save_event(request):
    application = Application.objects.filter(is_trusted=True)

    @sync_to_async
    def _save():
        event = Event(**json.loads(request.body))
        event.save()
        return event

    event = await _save()
    await event.process()

    return HttpResponse('event saved', status=201)
