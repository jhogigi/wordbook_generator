window.onload = function() {
    const request_task_status_page = () => {
        const element = document.getElementById('task-id')
        const task_id = element.dataset.taskid

        fetch(`/api/v1/tasks/${task_id}/`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((response) => response.json())
        .then((data) => {
            if (data == "SUCCESS") {
                window.location.href = `/task_result/${task_id}`
            } else if (data == "FAILURE") {
                alert("申し訳ございません。タスクの処理に失敗しました。")
                window.location.href = "/file_upload/"
            }
        })
    }
    setInterval(request_task_status_page, 10000);
} 