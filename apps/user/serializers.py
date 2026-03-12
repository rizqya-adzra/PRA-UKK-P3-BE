from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.validators import UniqueValidator
from .models import CoreUser, CoreStudent, CoreAdmin

class StudentRegisterSerializer(serializers.ModelSerializer):
    nis = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        error_messages={
            'required': 'Password wajib diisi.',
            'blank': 'Password tidak boleh kosong.',
            'min_length': 'Password minimal 6 karakter.'
        }
    )

    class Meta:
        model = CoreUser
        fields = ['email', 'password', 'nis', 'name']
        extra_kwargs = {
            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=CoreUser.objects.all(),
                        message='Email sudah terdaftar.'
                    )
                ],
                'error_messages': {
                    'required': 'Email wajib diisi.',
                    'invalid': 'Format email salah.'
                }
            },
        }

    def create(self, validated_data):
        nis = validated_data.pop('nis')
        name = validated_data.pop('name', None)
        email = validated_data.get('email')
        
        name = validated_data.pop('name', None)
        if not name:
            name = email.split('@')[0]

        with transaction.atomic():
            user = CoreUser.objects.create_user(**validated_data)
            
            CoreStudent.objects.create(
                user=user,
                nis=nis,
                name=name,
            )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={'required': 'Email wajib diisi.'})
    password = serializers.CharField(write_only=True, error_messages={'required': 'Password wajib diisi.'})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Email atau password salah.")


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreStudent
        fields = ['nis', 'name', 'rombel', 'rayon']

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreAdmin
        fields = ['name']


class MeSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = CoreUser
        fields = ['id', 'email', 'is_staff', 'profile', 'created_at']
        read_only_fields = ['email', 'is_staff', 'created_at']

    def get_profile(self, obj):
        if hasattr(obj, 'student_profile'):
            return StudentProfileSerializer(obj.student_profile).data
        if hasattr(obj, 'admin_profile'):
            return AdminProfileSerializer(obj.admin_profile).data
        return None