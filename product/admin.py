from django.contrib import admin
from .models import Files_upload,ProjectFilesUpload

# Register your models here.

@admin.register(Files_upload)
class Files_uploadAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectFilesUpload)
class ProjectFilesUploadAdmin(admin.ModelAdmin):
    pass