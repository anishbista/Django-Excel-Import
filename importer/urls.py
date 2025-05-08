from django.urls import path
from importer import views

urlpatterns = [
    path("import/", views.ImportProductView.as_view(), name="product-import"),
    path(
        "import/<uuid:pk>/",
        views.ImportJobDetailView.as_view(),
        name="import-job-detail",
    ),
]
