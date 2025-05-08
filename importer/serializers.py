from rest_framework import serializers
from .models import ImportJob, ImportLog


class ImportLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportLog
        fields = ["log_type", "row_number", "message", "created_at"]


class ImportJobSerializer(serializers.ModelSerializer):
    logs = ImportLogSerializer(many=True, read_only=True)

    class Meta:
        model = ImportJob
        fields = [
            "id",
            "file",
            "status",
            "started_at",
            "completed_at",
            "total_rows",
            "success_count",
            "warning_count",
            "error_count",
            "logs",
        ]
        read_only_fields = [
            "status",
            "started_at",
            "completed_at",
            "total_rows",
            "success_count",
            "warning_count",
            "error_count",
            "logs",
        ]
