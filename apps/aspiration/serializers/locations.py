from rest_framework import serializers
from apps.aspiration.models import Location

class LocationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Nama lokasi wajib diisi.',
            'blank': 'Nama lokasi tidak boleh kosong.'
        }
    )

    class Meta:
        model = Location
        fields = ['id', 'name']