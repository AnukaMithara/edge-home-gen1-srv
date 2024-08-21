from typing import Optional, Any


class GenericPaginationResponse:
    def __init__(self, is_error: bool, message: str, total_records: int, page_number: int, page_size: int,
                 total_pages: int, results: Optional[Any]):
        self.is_error = is_error
        self.message = message
        self.total_records = total_records
        self.page_number = page_number
        self.page_size = page_size
        self.total_pages = total_pages
        self.results = results

    @classmethod
    def success(cls, message: str, total_records, page_number, page_size, total_pages, results: Optional[Any]):
        return cls(is_error=False, message=message, total_records=total_records, page_number=page_number,
                   page_size=page_size, total_pages=total_pages, results=results)

    @classmethod
    def failed(cls, message: str, page_number, page_size, results: Optional[Any]):
        return cls(is_error=True, message=message, total_records=0, page_number=page_number,
                   page_size=page_size, total_pages=0, results=results)
