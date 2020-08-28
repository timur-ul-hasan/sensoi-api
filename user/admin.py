from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(Files_upload)
class UserAdmin(admin.ModelAdmin):
    pass
