import datetime

from django.core.files.storage import default_storage
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse

from file_manager.forms import UploadFileForm
from tasks.models import Task
from tasks.app import call_htmlparser


class FileManagerView(View):
    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, 'file_manager/upload.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            now_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            original_file = request.FILES['original_file']
            default_storage.save(now_date, original_file)
            task = Task.objects.create(original_file_path=now_date)
            call_htmlparser.delay(task.id)

        return HttpResponse(default_storage.url(now_date))
