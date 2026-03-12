from django.contrib import admin
from .models import Category, Aspiration, AspirationProgress, Notification

class AspirationProgressInline(admin.TabularInline):
    model = AspirationProgress
    extra = 1 
    readonly_fields = ('created_at',) 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Aspiration)
class AspirationAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'user', 'title', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('report_id', 'title', 'user__email', 'description')
    readonly_fields = ('report_id', 'created_at', 'updated_at')
    
    inlines = [AspirationProgressInline]
    
    fieldsets = (
        ('Informasi Utama', {
            'fields': ('report_id', 'user', 'title', 'category', 'status')
        }),
        ('Isi Aspirasi', {
            'fields': ('location', 'description', 'image', 'video')
        }),
        ('Audit Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AspirationProgress)
class AspirationProgressAdmin(admin.ModelAdmin):
    list_display = ('aspiration', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'aspiration', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'message')