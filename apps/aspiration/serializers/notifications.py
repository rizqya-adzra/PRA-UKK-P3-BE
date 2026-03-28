from rest_framework import serializers
from apps.aspiration.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    aspiration_info = serializers.SerializerMethodField()
    aspiration_id = serializers.UUIDField(source='aspiration.id', read_only=True)

    student_info = serializers.SerializerMethodField()
    student = serializers.CharField(source='aspiration.user.email', read_only=True)
    student_image = serializers.ImageField(source='user.image', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'message', 'student', 'student_image', 'student_info',
            'aspiration_id', 'aspiration_info',
            'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'message', 'created_at']

    def get_aspiration_info(self, obj):
        return {
            "report_id": obj.aspiration.report_id,
            "name": obj.aspiration.title,
            "location": obj.aspiration.location.name,
            "description": obj.aspiration.description,
            "category": obj.aspiration.category.name,
            "status": obj.aspiration.get_status_display(),
        }

    def get_student_info(self, obj):
        try:    
            student_profile = obj.aspiration.user.student_profile 
            return {
                "name": student_profile.name,
                "nis": student_profile.nis,
                "rombel": student_profile.rombel,
                "rayon": student_profile.rayon,
            }
        except:
            return None
        
    def get_student_info(self, obj):
        try:
            student_profile = obj.aspiration.user.student_profile 
            return {
                "name": student_profile.name,
                "nis": student_profile.nis,
                "rombel": student_profile.rombel,
                "rayon": student_profile.rayon,
            }
        except:
            return None