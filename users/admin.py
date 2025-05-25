from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import TrackerUser


@admin.register(TrackerUser)
class TrackerUserAdmin(UserAdmin):  # Наследуем от UserAdmin
    list_display = ('username', 'email', 'tg_id_chat', 'is_staff')  # Какие поля показывать
    list_filter = ('is_staff', 'is_superuser', 'is_active')  # По каким полям фильтровать
    search_fields = ('username', 'email', 'tg_id_chat')  # По каким полям искать
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'tg_id_chat')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
