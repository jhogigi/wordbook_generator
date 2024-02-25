class TaskStatusDTO:
    def __init__(self, status: str, detail: str):
        self.status = status
        self.detail = detail


class InquiryTaskStatusUsecase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, task_id) -> TaskStatusDTO:
        raise NotImplementedError()
