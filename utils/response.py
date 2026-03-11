from rest_framework.response import Response
from rest_framework import status

def response_success(message, data=None, status_code=status.HTTP_200_OK):
    return Response({
        "success": True,
        "message": message,
        "data": data
    }, status=status_code)

def response_error(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    formatted_errors = None
    
    if errors:
        formatted_errors = {}
        if isinstance(errors, dict):
            for key, val in errors.items():
                formatted_errors[key] = val[0] if isinstance(val, list) else str(val)
                if key == 'non_field_errors':
                    formatted_errors['detail'] = formatted_errors.pop('non_field_errors')
        else:
            formatted_errors = {"detail": str(errors)}

    return Response({
        "success": False,
        "message": message,
        "errors": formatted_errors
    }, status=status_code)