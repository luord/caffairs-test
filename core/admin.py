from django.contrib import admin

from core.models import Application, ValidationSchema, Event


admin.site.register(Application)
admin.site.register(ValidationSchema)
admin.site.register(Event)
