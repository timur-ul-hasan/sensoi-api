from django.db import models
from ..user.models import User

# Create your models here.
type_choices = (('csv', 'csv'), ('xlsx', 'xslsx'), ('xls', 'xls'),
                ('pdf', 'pdf'), ('txt', 'txt'), ('jpeg', 'jpeg'), ('jpg', 'jpg'))


def location_file(instance, filename):
    return f'users/{instance.user}/{filename}'


def location_project_file(instance, filename):
    return f'users/{instance.user}/{instance.project_name}/{filename}'


class Files_upload(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    up_file = models.FileField(upload_to=location_file, default=False, verbose_name='file')
    data_type = models.CharField(max_length=25, blank=False, choices=type_choices)
    name = models.CharField(max_length=150, default='Undefined')
    favorite = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.up_file}'

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'


class ProjectFilesUpload(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    up_file = models.FileField(upload_to=location_project_file, default=False, verbose_name='file')
    taxo_file = models.FileField(upload_to=location_project_file, default=False, verbose_name='taxo-file')
    name = models.CharField(max_length=150, default='Undefined')
    date = models.DateTimeField(auto_now_add=True)
    project_name = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return f'{self.up_file}'

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
