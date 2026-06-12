from django.contrib import admin

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    """Configure the user overview in the Django admin interface."""

    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)

admin.register(UserAdmin)
