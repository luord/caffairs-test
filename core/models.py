from django.db import models
from django.utils import timezone


class Application(models.Model):
    is_trusted = models.BooleanField(null=False, default=False)


class ValidationSchema(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    schema = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["category", "name"])
        ]


class Event(models.Model):
    session_id = models.UUIDField(editable=False)
    cateogry = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    data = models.JSONField()
    timestamp = models.DateTimeField()

    class ValidationStates(models.TextChoices):
        NON_VALIDATED = "NV", "Processing Pending"
        INVALID = "IN", "Invalid"
        VALID = "VA", "Valid"

    validation_state = models.CharField(
        max_length=2,
        choices=ValidationStates.choices,
        default=ValidationStates.NON_VALIDATED
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["category", "name", "session_id", "timestamp"])
        ]

    def process(self):
        if self.validation_state != ValidationStates.NON_VALIDATED:
            return

        if self.timestamp > timezone.now():
            self.validation_state = ValidationStates.INVALID

        try:
            self._match_schema(self.data)
            self.validation_state = ValidationStates.VALID
        except:
            self.validation_state = ValidationStates.INVALID

        self.save()

    def _match_schema(self, data):
        try:
            schema = ValidationSchema.objects.get(name=self.name, category=self.category)
        except models.DoesNotExist:
            return

        assert not schema.schema.keys().symmetric_difference(data.keys())

        # TODO: Iterate over schema and validate, for instance, types
