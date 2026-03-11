from rest_framework.views import exception_handler
from utils.response import response_error

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        
        error_message = "Terjadi kesalahan"
        if response.status_code == 400:
            error_message = "Validasi Gagal"
        elif response.status_code == 401:
            error_message = "Tidak terautentikasi"
        elif response.status_code == 403:
            error_message = "Akses ditolak"
        elif response.status_code == 404:
            error_message = "Data tidak ditemukan"
            
        return response_error(
            message=error_message,
            errors=response.data, 
            status_code=response.status_code
        )

    return response