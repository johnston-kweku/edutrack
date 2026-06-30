from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import User, Invitation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'full_name', 'username', 'role', 'contact', 'is_active', 'email', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['full_name', 'username', 'email', 'contact']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'title', 'contact', 'picture',)}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ['date_joined', 'last_login']
    

    def thumbnail(self, obj):
        if obj.picture:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />', obj.picture.url)
        return mark_safe('<div style="width: 40px; height: 40px; border-radius: 50%; background: #e2e8f0; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #64748b;">No Pic</div>')
    thumbnail.short_description = 'Pic'

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['role', 'created_by', 'created_at', 'expires_at', 'is_used']
    list_filter = ['role', 'is_used']