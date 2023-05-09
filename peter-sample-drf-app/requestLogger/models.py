from django.db import models

class APIRequestLog(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    request_data = models.JSONField(null=True)
    response_data = models.JSONField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.path} ({self.status_code})"

    class Meta:
        ordering = ['-timestamp']


class ModelChangeLog(models.Model):
    # user_id = models.BigIntegerField(null=False, blank=True, db_index=True)
    model_name = models.CharField(max_length=132)
    action_type = models.CharField(max_length=16, null=True, blank=True)
    instance_pk = models.IntegerField(null=True, blank=True)
    changes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"actionType: {self.action_type} -- Model: {self.model_name}"


