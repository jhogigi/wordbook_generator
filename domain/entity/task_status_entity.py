class TaskStatusEntity:
    def __init__(self, task_id: str, task_status: str):
        if task_id is None:
            raise ValueError('task_id is None')
        if task_status is None:
            raise ValueError('task_status is None')
        
        # FIXME あとでUUID型にする
        self.task_id: str = task_id
        self.task_status: str = task_status
        
    
    def get_task_status(self) -> str:
        return self.task_status
