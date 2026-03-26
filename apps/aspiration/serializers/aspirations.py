import os 
from rest_framework import serializers
from apps.aspiration.serializers.locations import LocationSerializer
from apps.aspiration.serializers.categories import CategorySerializer
from apps.aspiration.models import Location, Category, Aspiration, AspirationProgress, AspirationFile


class AspirationFileSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = AspirationFile
        fields = ['id', 'file', 'file_type']

    def validate_file(self, value):
        limit = 5 * 1024 * 1024
        if value.size > limit:
            raise serializers.ValidationError("Ukuran file tidak boleh lebih dari 5MB.")
        return value

    def get_file_type(self, obj):
        if not obj.file: 
            return None
        ext = os.path.splitext(obj.file.name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.webp']: return 'image'
        if ext in ['.mp4', '.mov']: return 'video'
        if ext in ['.pdf', '.doc', '.docx']: return 'document'
        return 'other'


class AspirationProgressSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.email', read_only=True)
    
    attachments = AspirationFileSerializer(many=True, read_only=True, source='progress_attachments')
    
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
        fields = ['id', 'aspiration', 'admin_name', 'status', 'description', 'attachments', 'created_at']
        read_only_fields = ['id', 'created_at']


class AspirationSerializer(serializers.ModelSerializer):
    location_detail = LocationSerializer(source='location', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    progress_updates = AspirationProgressSerializer(many=True, read_only=True)
    
    attachments = AspirationFileSerializer(many=True, read_only=True)
    
    student_info = serializers.SerializerMethodField()
    student_image = serializers.ImageField(source='user.image', read_only=True)

    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source='location',
        required=True,
        error_messages={
            'required': 'Lokasi wajib dipilih.',
            'null': 'Lokasi tidak boleh kosong.',
            'does_not_exist': 'Lokasi yang dipilih tidak ditemukan.'
        }
    )
    
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
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_color = serializers.SerializerMethodField()
    student = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Aspiration
        fields = [
            'id', 'report_id', 'student', 'student_image', 'student_info', 'title', 'description', 
            'location_id', 'location_detail',
            'category_id', 'category_detail', 
            'attachments', 
            'status', 'status_display', 'status_color',
            'progress_updates', 'created_at'
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
            }
        except:
            return None