class ItemCatalogError(Exception):
    status_code = 500


class ValidationError(ItemCatalogError):
    status_code = 400


class UnauthorizedError(ItemCatalogError):
    status_code = 401
