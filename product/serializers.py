from django import forms
from .models import Files_upload, ProjectFilesUpload
from user.models import User
from rest_framework.serializers import Serializer,ModelSerializer
from rest_framework import serializers
from .constants import TYPE_CHOICES

class FileInputSerializer(ModelSerializer):
    user = serializers.IntegerField()
    up_file = serializers.FileField()
    node_id = serializers.CharField()

    def validate_up_file(self, value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]  
        valid_extensions = [
            '.csv',
            '.pdf',
            '.jpg',
            '.jpeg',
            '.xlsx',
            '.xls',
            '.txt',
        ]
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')
        return value

    class Meta:
        model = Files_upload
        fields = ('up_file', 'user','node_id',)


class NodesSerializer(Serializer):
    nodes = serializers.ListField(
        child=serializers.CharField(max_length=200),
        allow_empty=True
    )

class FileUploadSerializer(ModelSerializer):
    class Meta:
        model = Files_upload
        fields = '__all__'



class ProjectFileInputSerializer(Serializer):
    up_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=True, use_url=True),
        required=True
    )

    txo_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=True, use_url=True),
        required=True
    )

    
    class Meta:
        fields = ('up_files','txo_files')

class ProjectFileInputSerializerSwagger(Serializer):
    up_files = serializers.ListField(
        child=serializers.URLField(),
        required=True
    )

    taxo_files = serializers.ListField(
        child=serializers.URLField(),
        required=True
    )





# class RenameForm(forms.Form):
#     new_name = forms.CharField(max_length=150, label='New Name')

#     class Meta:
#         fields = ('new_name',)


# class SearchForm(forms.Form):
#     search = forms.CharField(max_length=100)
