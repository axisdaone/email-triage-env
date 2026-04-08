# models.py
from pydantic import BaseModel
from typing import Optional, List

class Email(BaseModel):
    id: str
    subject: str
    sender: str
    body: str
    timestamp: str

class Observation(BaseModel):
    current_email: Email          # the email the agent is looking at
    inbox_remaining: int          # how many emails are left
    step_count: int               # how many steps taken so far
    task_id: str                  # which task we are on

class Action(BaseModel):
    label: str                    # e.g. "urgent", "not_urgent", "spam"
    folder: Optional[str] = None  # e.g. "work", "personal", "billing"
    reply_draft: Optional[str] = None  # only needed for task 3

class Reward(BaseModel):
    value: float                  # 0.0 to 1.0
    reason: str                   # human-readable explanation