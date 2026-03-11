from django.contrib import admin
from .models import CoreUser, CoreStudent, CoreAdmin

@admin.register(CoreUser)
class CoreUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    
    search_fields = ('email',)
    
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    
    ordering = ('-created_at',)
    
    readonly_fields = ('created_at', 'updated_at', 'password')

    fieldsets = (
        ('Informasi Akun', {'fields': ('email', 'password')}),
        ('Status Izin', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Grup & Hak Akses', {'fields': ('groups', 'user_permissions')}),
        ('Waktu', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(CoreStudent)
class CoreStudentAdmin(admin.ModelAdmin):
    list_display = ('nis', 'name', 'rombel', 'rayon', 'get_email')
    search_fields = ('nis', 'name', 'user__email')
    list_filter = ('rombel', 'rayon')
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email Akun'
    get_email.admin_order_field = 'user__email'

@admin.register(CoreAdmin)
class CoreAdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_email')
    search_fields = ('name', 'user__email')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email Akun'
    get_email.admin_order_field = 'user__email'