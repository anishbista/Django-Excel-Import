from django.db import models

from utils.common import CommonModel
from utils.enums import LOG_TYPES, STATUS_CHOICES


class ImportJob(CommonModel):

    file = models.FileField(upload_to="imports/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_rows = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    warning_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Import {self.id} - {self.status}"


class ImportLog(CommonModel):

    job = models.ForeignKey(ImportJob, on_delete=models.CASCADE, related_name="logs")
    log_type = models.CharField(max_length=10, choices=LOG_TYPES)
    row_number = models.IntegerField(null=True, blank=True)
    message = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.get_log_type_display()} at row {self.row_number}: {self.message[:50]}"
