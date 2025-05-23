class ProductValidator:
    @staticmethod
    def validate_required_fields(row_data, row_num):
        required_fields = [
            "id",
            "title",
            "description",
            "link",
            "image_link",
            "availability",
            "price",
            "condition",
            "brand",
            "gtin",
        ]
        errors = []

        for field in required_fields:
            if not row_data.get(field):
                errors.append(f"Missing required field: {field}")

        return errors

    @staticmethod
    def validate_warning_fields(row_data, row_num):
        warning_fields = [
            "sale_price",
            "item_group_id",
            "google_product_category",
            "product_type",
            "size",
            "color",
            "material",
            "pattern",
            "gender",
            "Model",
        ]
        warnings = []

        for field in warning_fields:
            if not row_data.get(field):
                warnings.append(f"Missing recommended field: {field}")

        return warnings

    @staticmethod
    def validate_price(row_data, row_num):
        warnings = []
        try:
            price_str = row_data.get("price", "0").replace(",", "").split()[0]
            price = float(price_str)
            if price <= 0:
                warnings.append("Price should be greater than 0")

            sale_price_str = row_data.get("sale_price", "").replace(",", "").split()[0]
            if sale_price_str:
                sale_price = float(sale_price_str)
                if sale_price <= 0:
                    warnings.append("Sale price should be greater than 0")
                if sale_price >= price:
                    warnings.append("Sale price should be less than regular price")

        except (ValueError, TypeError):
            return ["Invalid price format"]

        return warnings
