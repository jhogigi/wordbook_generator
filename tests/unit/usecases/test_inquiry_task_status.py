import pytest

from domain.entity.task_status_entity import TaskStatusEntity
from domain.repository.i_task_status_repository import ITaskStatusRepository
from domain.usecases.inquiry_task_status_usecase import InquiryTaskStatusUsecase, TaskStatusDTO


class TestInquiryTaskStatusUsecase:
    class DummyTaskStatusRepository(ITaskStatusRepository):
        def __init__(self) -> None:
            pass
        
        def get_by_task_id(self, task_id) -> TaskStatusEntity:
            return TaskStatusEntity(task_id=1, task_name='test', task_status='DONE')

    @pytest.mark.skip(reason="まだ実装してない")
    def test_Taskの処理状況を取得できる(self):
        task_status_repository = self.DummyTaskStatusRepository()
        
        result: TaskStatusDTO = InquiryTaskStatusUsecase(task_status_repository).execute()
        assert result.status == "DONE"
        assert result.detail == "HTML解析中です。"
        