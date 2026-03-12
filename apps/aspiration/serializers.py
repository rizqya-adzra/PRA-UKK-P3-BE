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
            'Infrastruktur': '#8e44ad',
            'Keamanan': '#c0392b',
            'Kebersihan': '#27ae60',
            'Lainnya': '#7f8c8d',
        }
        return mapping.get(obj.name, '#3498db')


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
    sender = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Aspiration
        fields = [
            'id', 'report_id', 'sender', 'title', 'description', 'location',
            'category_id', 'category_detail', 
            'status', 'status_display', 'status_color',
            'image', 'video', 'progress_updates', 'created_at'
        ]
        read_only_fields = ['id', 'report_id', 'status', 'created_at']

    def get_status_color(self, obj):
        mapping = {
            'menunggu': '#FFC107', 
            'proses': '#007BFF',   
            'selesai': '#28A745',  
            'dibatalkan': '#DC3545'
        }
        return mapping.get(obj.status, '#6C757D')


class NotificationSerializer(serializers.ModelSerializer):
    report_id = serializers.CharField(source='aspiration.report_id', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'report_id', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'report_id', 'message', 'created_at']