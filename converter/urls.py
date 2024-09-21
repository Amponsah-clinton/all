from django.urls import path
from . import views

app_name = 'converter'

urlpatterns = [
    path('', views.file_converter_view, name='upload_file'),
    path('download/<int:file_id>/', views.download_file_view, name='download_file'),
]
