from rest_framework.response import Response
from rest_framework import status

def response_success(message, data=None, status_code=status.HTTP_200_OK):
    count = 0
    if data is not None:
        if isinstance(data, (list, tuple)):
            count = len(data)
        elif hasattr(data, 'count'):
            count = data.count()
        elif isinstance(data, dict) and not data:
            count = 0
        else:
            count = 1 if data else 0

    return Response({
        "success": True,
        "status_code": status_code,
        "message": message,
        "count": count, 
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
        "status_code": status_code,
        "message": message,
        "errors": formatted_errors
    }, status=status_code)