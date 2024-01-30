
class Task:
    def __init__(self, task_type: str, data: dict):
        """
        Initialize a new Task instance.

        :param task_type: A string representing the type of the task.
        :param data: A dictionary containing the task's data.
        """
        self.task_type = task_type
        self.data = data