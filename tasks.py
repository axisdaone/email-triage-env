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

    # Task 1: just label (worth 1.0 full score)
    if task_id == "task1":
        if action.label == email["correct_label"]:
            score = 1.0
        elif action.label in ["urgent", "not_urgent", "spam"]:
            score = 0.1  # tried but wrong
        return score

    # Task 2: label (0.5) + folder (0.5)
    if task_id == "task2":
        if action.label == email["correct_label"]:
            score += 0.5
        if action.folder == email["correct_folder"]:
            score += 0.5
        return score

    # Task 3: label (0.3) + folder (0.3) + reply draft (0.4)
    if task_id == "task3":
        if action.label == email["correct_label"]:
            score += 0.3
        if action.folder == email["correct_folder"]:
            score += 0.3
        # Reply only matters for urgent emails
        if email["correct_label"] == "urgent":
            if action.reply_draft and len(action.reply_draft) > 20:
                score += 0.4  # gave a real reply
            elif action.reply_draft:
                score += 0.1  # tried but too short
        else:
            score += 0.4  # non-urgent: no reply needed, give full points
        return score

    return 0.0