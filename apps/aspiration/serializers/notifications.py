from rest_framework import serializers
from apps.aspiration.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    report_id = serializers.CharField(source='aspiration.report_id', read_only=True)
    aspiration_title = serializers.CharField(source='aspiration.title', read_only=True)
    aspiration_description = serializers.CharField(source='aspiration.description', read_only=True)
    
    student_info = serializers.SerializerMethodField()
    student = serializers.CharField(source='aspiration.user.email', read_only=True)
    student_image = serializers.ImageField(source='user.image', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id',  'report_id', 'message', 'student', 'student_image', 'student_info',
            'aspiration_title', 'aspiration_description', 
            'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'report_id', 'message', 'created_at']

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