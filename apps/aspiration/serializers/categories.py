from rest_framework import serializers
from apps.aspiration.models import Category

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