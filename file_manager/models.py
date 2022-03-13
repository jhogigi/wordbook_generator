from email.policy import default
import uuid
from django.db import models


class TaskFiles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_file_path = models.CharField(max_length=100)
    task_id = models.UUIDField(default=uuid.uuid4)
