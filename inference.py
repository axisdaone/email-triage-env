# inference.py
import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN") or os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
ENV_URL = os.getenv("ENV_URL", "http://localhost:8000")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

SYSTEM_PROMPT = """You are an email triage agent. For each email you receive, respond with a JSON object containing:
- "label": one of "urgent", "not_urgent", or "spam"
- "folder": one of "work", "billing", or "spam"  
- "reply_draft": a short reply if the email is urgent, otherwise null

Respond ONLY with valid JSON, no other text."""

def run_task(task_id: str):
    print(f"\n--- Running {task_id} ---")
    obs = requests.post(f"{ENV_URL}/reset", params={"task_id": task_id}).json()
    total_reward = 0.0
    steps = 0

    while True:
        email = obs["current_email"]
        prompt = f"""Subject: {email['subject']}
From: {email['sender']}
Body: {email['body']}

Triage this email."""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.1,
        )

        raw = response.choices[0].message.content.strip()
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"label": "not_urgent", "folder": "work", "reply_draft": None}

        result = requests.post(f"{ENV_URL}/step", json=parsed).json()
        total_reward += result["reward"]["value"]
        steps += 1
        print(f"  Step {steps}: label={parsed.get('label')} | reward={result['reward']['value']:.2f}")

        if result["done"]:
            break
        obs = result["observation"]

    avg = total_reward / steps
    print(f"  Final: total={total_reward:.2f}, avg={avg:.2f}")
    return avg

if __name__ == "__main__":
    scores = {}
    for task in ["task1", "task2", "task3"]:
        scores[task] = run_task(task)
    print("\n=== Baseline Scores ===")
    for task, score in scores.items():
        print(f"  {task}: {score:.3f}")