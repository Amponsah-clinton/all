import os
import pypandoc
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import FileUploadForm
from .models import FileUpload
from django.http import HttpResponse

def file_converter_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['uploaded_file']
            target_format = form.cleaned_data['target_format']

            # Save the uploaded file
            file_instance = FileUpload(
                uploaded_file=uploaded_file,
                original_format=uploaded_file.name.split('.')[-1],
                target_format=target_format
            )
            file_instance.save()

            # Convert the file
            input_path = file_instance.uploaded_file.path
            output_path = f"{settings.MEDIA_ROOT}/converted/{uploaded_file.name}.{target_format}"

            try:
                pypandoc.convert_file(input_path, target_format, outputfile=output_path)
                file_instance.converted_file.name = f"converted/{uploaded_file.name}.{target_format}"
                file_instance.save()

                # Redirect to the download page
                return redirect('converter:download_file', file_id=file_instance.id)
            except Exception as e:
                return HttpResponse(f"Error during conversion: {e}")

    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def download_file_view(request, file_id):
    file_instance = FileUpload.objects.get(id=file_id)
    file_path = file_instance.converted_file.path
    file_name = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
