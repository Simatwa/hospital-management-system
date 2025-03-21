class HospitalException(Exception):
    """Base exception class for Hospital app"""


class InsufficientMedicineStockError(HospitalException):
    """Raised when medicine amount required is more that avaialable stock"""
