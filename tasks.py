# tasks.py
import random

EMAILS = [
    {
        "id": "e1", "subject": "URGENT: Server down in production",
        "sender": "devops@company.com", "body": "Production is down, customers affected!",
        "timestamp": "2024-01-15T09:00:00",
        "correct_label": "urgent", "correct_folder": "work"
    },
    {
        "id": "e2", "subject": "Your invoice is ready",
        "sender": "billing@service.com", "body": "Your monthly invoice of $49 is attached.",
        "timestamp": "2024-01-15T09:05:00",
        "correct_label": "not_urgent", "correct_folder": "billing"
    },
    {
        "id": "e3", "subject": "Congratulations! You won a prize!",
        "sender": "noreply@winner123.com", "body": "Click here to claim your $1000 prize!!",
        "timestamp": "2024-01-15T09:10:00",
        "correct_label": "spam", "correct_folder": "spam"
    },
    {
        "id": "e4", "subject": "Team lunch tomorrow",
        "sender": "manager@company.com", "body": "Are you joining team lunch at noon tomorrow?",
        "timestamp": "2024-01-15T09:15:00",
        "correct_label": "not_urgent", "correct_folder": "work"
    },
    {
        "id": "e5", "subject": "Security alert: New login detected",
        "sender": "security@bank.com", "body": "A new login was detected on your account from Mumbai.",
        "timestamp": "2024-01-15T09:20:00",
        "correct_label": "urgent", "correct_folder": "billing"
    },
]

TASKS = {
    "task1": {
        "description": "Label each email as urgent, not_urgent, or spam.",
        "difficulty": "easy",
        "emails": EMAILS[:3],
    },
    "task2": {
        "description": "Label each email AND route it to the correct folder: work, billing, or spam.",
        "difficulty": "medium",
        "emails": EMAILS[:4],
    },
    "task3": {
        "description": "Label, route, AND write a short professional reply draft for urgent emails.",
        "difficulty": "hard",
        "emails": EMAILS,
    },
}

def grade_action(task_id: str, email: dict, action) -> float:
    score = 0.0

    if task_id == "task1":
        if action.label == email["correct_label"]:
            score = 0.95
        else:
            score = 0.1
        return score

    if task_id == "task2":
        if action.label == email["correct_label"]:
            score += 0.45
        if action.folder == email["correct_folder"]:
            score += 0.45
        return max(0.01, min(0.99, score))

    if task_id == "task3":
        if action.label == email["correct_label"]:
            score += 0.28
        if action.folder == email["correct_folder"]:
            score += 0.28
        if email["correct_label"] == "urgent":
            if action.reply_draft and len(action.reply_draft) > 20:
                score += 0.38
            elif action.reply_draft:
                score += 0.1
        else:
            score += 0.38
        return max(0.01, min(0.99, score))

    return 0.01