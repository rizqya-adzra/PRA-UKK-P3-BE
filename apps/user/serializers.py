from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.validators import UniqueValidator
from .models import CoreUser, CoreStudent, CoreAdmin

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction


class StudentRegisterSerializer(serializers.ModelSerializer):
    nis = serializers.IntegerField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=CoreStudent.objects.all(),
                message='NIS ini sudah terdaftar.'
            )
        ],
        error_messages={
            'required': 'NIS wajib diisi.',
            'null': 'NIS tidak boleh kosong.',
            'invalid': 'NIS harus berupa angka.'
        }
    )
    
    name = serializers.CharField(
        max_length=255, 
        required=False, 
        allow_blank=True,
        error_messages={
            'max_length': 'Nama terlalu panjang (maksimal 255 karakter).'
        }
    )
    
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
                    'blank': 'Email tidak boleh kosong.',
                    'invalid': 'Format email salah.'
                }
            },
        }

    def create(self, validated_data):
        nis = validated_data.pop('nis')
        name = validated_data.pop('name', None)
        email = validated_data.get('email')
        
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
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = self.initial_data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Konfirmasi password tidak cocok."
            })
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': 'Email wajib diisi.',
            'blank': 'Email wajib diisi.',
            'invalid': 'Format email tidak valid.'
        }
    )
    password = serializers.CharField(
        write_only=True, 
        error_messages={
            'required': 'Password wajib diisi.',
            'blank': 'Password wajib diisi.'
        }
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password) 
            if not user:
                raise serializers.ValidationError({"detail": "Email atau password salah."})
            
            if not user.is_active:
                raise serializers.ValidationError({"detail": "Akun ini tidak aktif."})
        else:
            raise serializers.ValidationError({"detail": "Email dan password wajib diisi."})

        return user


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
        fields = ['id', 'email', 'image', 'is_staff', 'profile', 'created_at']
        read_only_fields = ['email', 'is_staff', 'created_at']

    def get_profile(self, obj):
        if hasattr(obj, 'student_profile'):
            return StudentProfileSerializer(obj.student_profile).data
        if hasattr(obj, 'admin_profile'):
            return AdminProfileSerializer(obj.admin_profile).data
        return None

    def update(self, instance, validated_data):
        profile_data = self.context['request'].data.get('profile')
        
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        if profile_data:
            if hasattr(instance, 'student_profile'):
                student_serializer = StudentProfileSerializer(
                    instance.student_profile, 
                    data=profile_data, 
                    partial=True
                )
                if student_serializer.is_valid(raise_exception=True):
                    student_serializer.save()
            
            elif hasattr(instance, 'admin_profile'):
                admin_serializer = AdminProfileSerializer(
                    instance.admin_profile, 
                    data=profile_data, 
                    partial=True
                )
                if admin_serializer.is_valid(raise_exception=True):
                    admin_serializer.save()

        return instance
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Password lama salah.")
        return value
    
class UserAspirationRankingSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    nis = serializers.SerializerMethodField()
    rombel = serializers.SerializerMethodField()
    aspiration_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CoreUser
        fields = ['id', 'email', 'name', 'nis', 'rombel', 'image', 'aspiration_count']

    def get_name(self, obj):
        if hasattr(obj, 'student_profile') and obj.student_profile:
            return obj.student_profile.name
        if hasattr(obj, 'admin_profile') and obj.admin_profile:
            return obj.admin_profile.name
        return obj.email.split('@')[0]

    def get_nis(self, obj):
        if hasattr(obj, 'student_profile') and obj.student_profile:
            return obj.student_profile.nis
        return None

    def get_rombel(self, obj):
        if hasattr(obj, 'student_profile') and obj.student_profile:
            return obj.student_profile.rombel
        return None