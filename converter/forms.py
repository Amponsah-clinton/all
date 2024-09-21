from django import forms

class FileUploadForm(forms.Form):
    uploaded_file = forms.FileField()
    target_format = forms.ChoiceField(choices=[
        ('pdf', 'PDF'),
        ('html', 'HTML'),
        ('docx', 'DOCX'),
        ('txt', 'Text'),
    ])
