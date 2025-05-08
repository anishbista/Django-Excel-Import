from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.db import transaction
from .models import ImportJob, ImportLog
from .serializers import ImportJobSerializer, ImportLogSerializer
from utils.excel_processor import ExcelProductProcessor
import threading
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    post=extend_schema(
        operation_id="import_products",
        summary="Import products from Excel",
        description="Upload an Excel file to import product data in bulk",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Excel file with product data",
                    }
                },
            }
        },
    )
)
class ImportProductView(generics.CreateAPIView):
    parser_classes = [MultiPartParser]
    queryset = ImportJob.objects.all()
    serializer_class = ImportJobSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not file.name.endswith(".xlsx"):
            return Response(
                {"error": "Only Excel (.xlsx) files are supported"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        import_job = ImportJob.objects.create(file=file)

        # Process in background
        def process_import():
            try:
                processor = ExcelProductProcessor(import_job.id)
                processor.process()
            except Exception as e:
                import_job.status = "failed"
                import_job.save()
                ImportLog.objects.create(
                    job=import_job,
                    log_type="error",
                    message=f"Processing failed: {str(e)}",
                )

        thread = threading.Thread(target=process_import)
        thread.start()

        return Response(
            ImportJobSerializer(import_job).data, status=status.HTTP_201_CREATED
        )


@extend_schema_view(
    get=extend_schema(
        operation_id="get_import_job_details",
        summary="Get import job details",
        description="Retrieve details of a specific import job, including logs",
    )
)
class ImportJobDetailView(generics.RetrieveAPIView):
    queryset = ImportJob.objects.all()
    serializer_class = ImportJobSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        logs = ImportLog.objects.filter(job=instance)
        log_serializer = ImportLogSerializer(logs, many=True)

        response_data = serializer.data
        response_data["logs"] = log_serializer.data

        return Response(response_data)
