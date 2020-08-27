from django import forms
from user.models import User
from .models import Files_upload, ProjectFilesUpload

class FileInputForm(forms.ModelForm):
    up_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    def save(self, *args, **kwargs):
        print(self.cleaned_data['up_file'])
        return super().save(commit=False)

    class Meta:
        model = Files_upload
        fields = ('up_file', 'user')


class ProjectFileInputForm(forms.ModelForm):
    up_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    taxo_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    def save(self, *args, **kwargs):
        return super().save(commit=False)

    # def __init__(self, *args, **kwargs):
    #     qs = kwargs.pop('user')
    #     super(FooForm, self).__init__(*args, **kwargs)
    #     self.fields['ingested'].queryset = qs

    class Meta:
        model = ProjectFilesUpload
        fields = ('up_file', 'user', 'taxo_file')

class RenameForm(forms.Form):
    new_name = forms.CharField(max_length=150, label='New Name')

    class Meta:
        fields = ('new_name',)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)
