from django import forms


class UploadFileForm(forms.Form):
    original_file = forms.FileField()

    def clean_original_file(self):
        original_file = self.cleaned_data['original_file']
        if not original_file.name.endswith('.html'):
            raise forms.ValidationError(".html以外のファイルがアップロードされました。ファイルの拡張子をご確認ください。")
        return original_file