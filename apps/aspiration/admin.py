from django.contrib import admin
from .models import Category, Aspiration, AspirationProgress, Notification, AspirationFile, Location


class AspirationFileInline(admin.TabularInline):
    model = AspirationFile
    fk_name = 'aspiration'
    extra = 1
    fields = ('file',) 
    verbose_name = "File Bukti Aspirasi"
    verbose_name_plural = "File Bukti Aspirasi"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(progress__isnull=True)

class ProgressFileInline(admin.TabularInline):
    model = AspirationFile
    fk_name = 'progress'
    extra = 1
    fields = ('file',)
    verbose_name = "File Bukti Progress"
    verbose_name_plural = "File Bukti Progress"

class AspirationProgressInline(admin.TabularInline):
    model = AspirationProgress
    extra = 1 
    readonly_fields = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Aspiration)
class AspirationAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'id', 'user', 'title', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('report_id', 'title', 'user__email', 'description')
    readonly_fields = ('report_id', 'created_at', 'updated_at')
    
    inlines = [AspirationFileInline, AspirationProgressInline]
    
    fieldsets = (
        ('Informasi Utama', {
            'fields': ('report_id', 'user', 'title', 'category', 'status')
        }),
        ('Isi Aspirasi', {
            'fields': ('location', 'description')
        }),
        ('Audit Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AspirationProgress)
class AspirationProgressAdmin(admin.ModelAdmin):
    list_display = ('aspiration', 'status', 'admin', 'created_at')
    list_filter = ('status', 'created_at')
    
    inlines = [ProgressFileInline]
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        
        for obj in formset.deleted_objects:
            obj.delete()
            
        for instance in instances:
            if isinstance(instance, AspirationFile):
                if not getattr(instance, 'aspiration_id', None):
                    instance.aspiration = instance.progress.aspiration
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        if not obj.admin:
            obj.admin = request.user
        super().save_model(request, obj, form, change)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'aspiration', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'message')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at')
    search_fields = ('name',)