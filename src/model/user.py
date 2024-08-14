from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional
from uuid import uuid4


# class Role(Enum):
#     ADMIN = "admin"
#     MASTER = "master"
#     LEARNER = "learner"


# class Status(Enum):
#     ENABLED = "enabled"
#     BLOCKED = "blocked"
#     DISABLED = "disabled"


@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid4()), init=False)
    username: str
    email: str
    name: str
    role: str
    status: str
    createdOn: datetime = field(default_factory=datetime.utcnow, init=False)
    createdBy: Optional[str] = None
    updatedOn: Optional[datetime] = None
    updatedBy: Optional[str] = None
    

    def __post_init__(self):
        self.validate_unique_fields()

    def validate_unique_fields(self):
        # Implement logic to check the uniqueness of username and email
        pass
