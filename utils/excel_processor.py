import pandas as pd
from django.db import transaction
from products.models import Product
from importer.models import ImportJob, ImportLog
from utils.validators import ProductValidator


class ExcelProductProcessor:
    def __init__(self, import_job_id):
        self.import_job = ImportJob.objects.get(id=import_job_id)
        self.chunk_size = 100

    def process(self):
        try:
            self.import_job.status = "processing"
            self.import_job.save()

            # Read Excel in chunks
            excel_file = self.import_job.file.path
            reader = pd.read_excel(excel_file, chunksize=self.chunk_size)

            total_rows = 0
            success_count = 0
            warning_count = 0
            error_count = 0

            for chunk in reader:
                chunk_rows = len(chunk)
                total_rows += chunk_rows

                for index, row in chunk.iterrows():
                    row_num = index + 2  # Excel rows start at 1, header at 1
                    row_data = row.to_dict()

                    # Validate
                    errors = ProductValidator.validate_required_fields(
                        row_data, row_num
                    )
                    warnings = ProductValidator.validate_warning_fields(
                        row_data, row_num
                    )
                    price_warnings = ProductValidator.validate_price(row_data, row_num)
                    warnings.extend(price_warnings)

                    if errors:
                        error_count += 1
                        for error in errors:
                            self._log_error(row_num, error)
                        continue

                    # Process row
                    try:
                        with transaction.atomic():
                            product = self._create_product(row_data)
                            success_count += 1

                            for warning in warnings:
                                warning_count += 1
                                self._log_warning(row_num, warning)

                    except Exception as e:
                        error_count += 1
                        self._log_error(row_num, str(e))

            # Update job status
            self.import_job.status = "completed"
            self.import_job.total_rows = total_rows
            self.import_job.success_count = success_count
            self.import_job.warning_count = warning_count
            self.import_job.error_count = error_count
            self.import_job.save()

        except Exception as e:
            self.import_job.status = "failed"
            self.import_job.save()
            raise

    def _create_product(self, row_data):
        product_data = {
            "sku": row_data["id"],
            "title": row_data["title"],
            "description": row_data["description"],
            "link": row_data["link"],
            "image_link": row_data["image_link"],
            "availability": row_data["availability"],
            "price": row_data["price"],
            "condition": row_data["condition"],
            "brand": row_data["brand"],
            "gtin": row_data["gtin"],
            "sale_price": row_data.get("sale_price"),
            "item_group_id": row_data.get("item_group_id"),
            "google_product_category": row_data.get("google_product_category"),
            "product_type": row_data.get("product_type"),
            "size": row_data.get("size"),
            "color": row_data.get("color"),
            "material": row_data.get("material"),
            "pattern": row_data.get("pattern"),
            "gender": row_data.get("gender"),
            "model": row_data.get("Model"),
        }

        # Clean empty strings
        for key, value in product_data.items():
            if isinstance(value, str) and not value.strip():
                product_data[key] = None

        product, created = Product.objects.update_or_create(
            sku=product_data["sku"], defaults=product_data
        )
        return product

    def _log_error(self, row_num, message):
        ImportLog.objects.create(
            job=self.import_job, log_type="error", row_number=row_num, message=message
        )

    def _log_warning(self, row_num, message):
        ImportLog.objects.create(
            job=self.import_job, log_type="warning", row_number=row_num, message=message
        )
