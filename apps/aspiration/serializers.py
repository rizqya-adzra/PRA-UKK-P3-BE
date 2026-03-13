from rest_framework import serializers
from .models import Category, Aspiration, AspirationProgress, Notification

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Nama kategori wajib diisi.',
            'blank': 'Nama kategori tidak boleh kosong.'
        }
    )
    color = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color']

    def get_color(self, obj):
        mapping = {
            'fasilitas': '#6D5DFF',
            'lingkungan': '#9DC344',
            'pendidikan': '#C03648',
            'karakter': '#C08736',
            'ibadah': '#BA36C0',
        }
        return mapping.get(obj.name.lower(), '#6C757D')


class AspirationProgressSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.email', read_only=True)
    
    status = serializers.ChoiceField(
        choices=Aspiration.STATUS_CHOICES,
        required=True,
        error_messages={
            'required': 'Status wajib diisi.',
            'invalid_choice': 'Pilihan status tidak valid.'
        }
    )
    description = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Deskripsi progress wajib diisi.',
            'blank': 'Deskripsi progress tidak boleh kosong.'
        }
    )

    class Meta:
        model = AspirationProgress
        fields = ['id', 'aspiration', 'admin_name', 'status', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class AspirationSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    progress_updates = AspirationProgressSerializer(many=True, read_only=True)
    student_info = serializers.SerializerMethodField()
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        required=True,
        error_messages={
            'required': 'Kategori wajib dipilih.',
            'null': 'Kategori tidak boleh kosong.',
            'does_not_exist': 'Kategori yang dipilih tidak ditemukan.'
        }
    )
    
    title = serializers.CharField(
        required=True,
        max_length=255,
        error_messages={
            'required': 'Judul aspirasi wajib diisi.',
            'blank': 'Judul aspirasi tidak boleh kosong.',
            'max_length': 'Judul terlalu panjang (maksimal 255 karakter).'
        }
    )
    description = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Deskripsi aspirasi wajib diisi.',
            'blank': 'Deskripsi aspirasi tidak boleh kosong.'
        }
    )
    location = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Lokasi kejadian wajib diisi.',
            'blank': 'Lokasi kejadian tidak boleh kosong.'
        }
    )
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_color = serializers.SerializerMethodField()
    student = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Aspiration
        fields = [
            'id', 'report_id', 'student', 'student_info', 'title', 'description', 'location',
            'category_id', 'category_detail', 
            'status', 'status_display', 'status_color',
            'image', 'video', 'progress_updates', 'created_at'
        ]
        read_only_fields = ['id', 'report_id', 'status', 'created_at']

    def get_status_color(self, obj):
        mapping = {
            'menunggu': '#EE9300', 
            'proses': '#006EFF',   
            'selesai': '#19A229',  
            'dibatalkan': '#A21919'
        }
        return mapping.get(obj.status.lower(), '#6C757D')
    
    def get_student_info(self, obj):
        try:
            student = obj.user.student_profile 
            return {
                "name": student.name,
                "nis": student.nis,
                "rombel": student.rombel,
                "rayon": student.rayon,
                # "image": student.image.url if student.image else None
            }
        except:
            return None


class NotificationSerializer(serializers.ModelSerializer):
    report_id = serializers.CharField(source='aspiration.report_id', read_only=True)
    aspiration_title = serializers.CharField(source='aspiration.title', read_only=True)
    aspiration_description = serializers.CharField(source='aspiration.description', read_only=True)
    
    student_info = serializers.SerializerMethodField()
    student = serializers.CharField(source='aspiration.user.email', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id',  'report_id', 'message', 'student', 'student_info',
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
                # "image": student.image.url if student.image else None
            }
        except:
            return None