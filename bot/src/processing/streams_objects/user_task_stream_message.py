from typing import Dict
import json


class UserTaskStreamMessage:
    def __init__(self, task_id: int, task_type: str, payload: dict, user_id: int):
        self.task_id = task_id
        self.task_type = task_type
        self.payload = payload
        self.user_id = user_id

    def to_dict(self) -> Dict[str, str]:
        return {
            "task_id": str(self.task_id),
            "task_type": self.task_type,
            "payload": json.dumps(self.payload),
            "user_id": str(self.user_id),
        }