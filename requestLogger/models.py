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
