from django import forms


class UploadFileForm(forms.Form):
    """
    TODO
    validationの追加 html, txtファイル以外を排除する
    """
    original_file = forms.FileField()
