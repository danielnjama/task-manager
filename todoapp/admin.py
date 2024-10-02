from django.contrib import admin
from django.utils.html import format_html
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status_color', 'created_at','marked')
    list_filter = ('completed','marked')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

    def status_color(self, obj):
        if obj.completed:
            return format_html('<span style="color: green;">Completed</span>')
        return format_html('<span style="color: red;">Pending</span>')
    
    status_color.short_description = 'Status'

    # Override get_queryset to restrict all users (including superusers) to their own todos
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)  # Everyone, including superusers, can only see their own todos

    # Remove the user field from the form altogether
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'user' in form.base_fields:
            del form.base_fields['user']  # Remove the user field completely from the form
        return form

    # Automatically assign the logged-in user as the owner when saving a new todo
    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.user = request.user  # Set the current user as the owner
        super().save_model(request, obj, form, change)

admin.site.register(Todo, TodoAdmin)
