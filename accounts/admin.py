from django.contrib import admin
from .models import User, Invitation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'role', 'contact', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['full_name', 'username', 'email']

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['role', 'created_by', 'created_at', 'expires_at', 'is_used']
    list_filter = ['role', 'is_used']