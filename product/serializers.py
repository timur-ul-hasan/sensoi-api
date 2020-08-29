from django import forms
from .models import Files_upload, ProjectFilesUpload
from user.models import User
from rest_framework.serializers import Serializer,ModelSerializer
from rest_framework import serializers
from .constants import TYPE_CHOICES


# class FileInputForm(forms.ModelForm):
#     up_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
#     user = forms.ModelChoiceField(queryset=Users.objects.all(), widget=forms.HiddenInput())

#     def save(self, *args, **kwargs):
#         print(self.cleaned_data['up_file'])
#         return super().save(commit=False)

#     class Meta:
#         model = Files_upload
#         fields = ('up_file', 'user')


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



# class ProjectFileInputForm(forms.ModelForm):
#     up_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
#     taxo_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
#     user = forms.ModelChoiceField(queryset=Users.objects.all(), widget=forms.HiddenInput())

#     def save(self, *args, **kwargs):
#         return super().save(commit=False)

#     # def __init__(self, *args, **kwargs):
#     #     qs = kwargs.pop('user')
#     #     super(FooForm, self).__init__(*args, **kwargs)
#     #     self.fields['ingested'].queryset = qs

#     class Meta:
#         model = ProjectFilesUpload
#         fields = ('up_file', 'user', 'taxo_file')

# class RenameForm(forms.Form):
#     new_name = forms.CharField(max_length=150, label='New Name')

#     class Meta:
#         fields = ('new_name',)


# class SearchForm(forms.Form):
#     search = forms.CharField(max_length=100)
