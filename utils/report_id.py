from django.utils import timezone
import datetime

def generate_report_id(model_class):
    today = timezone.now().strftime('%Y%m%d') 
    prefix = f"REP-{today}-"

    last_report = model_class.objects.filter(
        report_id__icontains=prefix
    ).order_by('-report_id').first()

    if not last_report:
        new_number = "0001"
    else:
        last_number = int(last_report.report_id.split('-')[-1])
        new_number = f"{last_number + 1:04d}" 

    return f"{prefix}{new_number}"