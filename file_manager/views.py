import datetime

from django.core.files.storage import default_storage
from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect
import pandas as pd

from file_manager.forms import UploadFileForm
from tasks.models import Task
from tasks.app import get_task_chain


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

            chain = get_task_chain(task.id)
            async_result = chain.apply_async()
            task.async_result_id = async_result.task_id
            task.save()
        return redirect(f'/waiting_task/{task.id}/')


class WaitingTaskPage(TemplateView):
    template_name ='file_manager/waiting_task.html'

    def get_context_data(self, task_id, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['task_id'] = task_id
        return ctx


class ResultTaskPage(TemplateView):
    template_name = 'file_manager/result_task.html'

    def get_context_data(self, task_id, **kwargs):
        task = Task.objects.get(id=task_id)
        df = pd.read_csv(task.output_file_path, index_col=0)
        now= datetime.datetime.now()

        ctx = super().get_context_data(**kwargs)
        ctx['csv_download_path'] = task.output_file_path
        ctx['csv_download_name'] = f'{now}.csv'
        ctx['data'] = df.head(50).to_dict(orient="records")
        return ctx
