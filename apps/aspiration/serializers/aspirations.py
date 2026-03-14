from rest_framework import serializers
from apps.aspiration.serializers.categories import CategorySerializer
from apps.aspiration.models import Category, Aspiration, AspirationProgress


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