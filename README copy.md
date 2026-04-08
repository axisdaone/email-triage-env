# Email Triage Environment

An OpenEnv-compatible reinforcement learning environment where an AI agent learns to triage a realistic email inbox — labelling urgency, routing to folders, and drafting replies.

## Why this environment?

Email triage is one of the most universal productivity tasks humans do every day. This environment trains and evaluates agents on realistic inbox scenarios with clear, measurable success criteria — making it immediately useful for anyone building AI assistants or productivity agents.

## Environment description

The agent is presented with emails one at a time from a simulated inbox. For each email, it must decide how to handle it. Tasks increase in complexity from simple labelling to full triage with reply drafting.

The environment tracks partial progress — an agent that gets the label right but the folder wrong still earns partial reward, rather than getting zero. This gives a much richer training signal than binary pass/fail.

## Action space

The agent submits a JSON action for each email:

| Field | Type | Values | Required |
|-------|------|---------|----------|
| label | string | urgent, not_urgent, spam | always |
| folder | string | work, billing, spam | task 2 and 3 |
| reply_draft | string | any text | task 3 only (for urgent emails) |

## Observation space

The agent receives a JSON observation for each step:

| Field | Type | Description |
|-------|------|-------------|
| current_email | object | id, subject, sender, body, timestamp |
| inbox_remaining | int | emails left in the inbox |
| step_count | int | how many steps taken so far |
| task_id | string | which task is currently running |

## Tasks

### Task 1 — Label urgency (easy)
Classify each email as urgent, not_urgent, or spam.
- 3 emails
- Reward: 1.0 for correct label, 0.1 for wrong label
- Baseline score: 1.000

### Task 2 — Label and route (medium)
Classify each email AND route it to the correct folder (work, billing, spam).
- 4 emails
- Reward: 0.5 for correct label + 0.5 for correct folder
- Baseline score: 1.000

### Task 3 — Triage and reply (hard)
Classify, route, AND write a professional reply draft for urgent emails.
- 5 emails
- Reward: 0.3 label + 0.3 folder + 0.4 reply quality
- Baseline score: 0.940

## Reward function

Rewards are shaped to give partial credit at every step:

- Correct label alone is always worth something
- Correct folder adds more
- A meaningful reply draft (over 20 characters) earns full reply points
- No binary end-of-episode scoring — every step gives signal

This design means an agent improves gradually and does not get stuck with zero reward during early training.

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /reset?task_id=task1 | Start a new episode |
| POST | /step | Submit an action, get observation + reward |
| GET | /state | Inspect current environment state |
| GET | /docs | Interactive API documentation |

## Setup

### Run locally
```bash
git clone https://huggingface.co/spaces/your-username/email-triage-env
cd email-triage-env
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic openai requests
uvicorn main:app --reload
```

Visit http://localhost:8000/docs to explore the API interactively.

### Run with Docker
```bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
```

## Run baseline inference
```bash
export HF_TOKEN="your-token-here"
export MODEL_NAME="meta-llama/Llama-3.3-70B-Instruct"
export API_BASE_URL="https://router.huggingface.co/v1"
export ENV_URL="http://localhost:8000"

python inference.py
```

## Baseline scores

Evaluated using meta-llama/Llama-3.3-70B-Instruct via Hugging Face Inference Router.

| Task | Difficulty | Score |
|------|------------|-------|
| task1 | Easy | 1.000 |
| task2 | Medium | 1.000 |
| task3 | Hard | 0.940 |

## Project structure
```
email-triage-env/
├── main.py          # FastAPI server with reset/step/state endpoints
├── models.py        # Pydantic models for Observation, Action, Reward
├── tasks.py         # Task definitions and graders
├── inference.py     # Baseline agent using OpenAI-compatible client
├── openenv.yaml     # OpenEnv metadata
├── Dockerfile       # Container definition
└── README.md        # This file
```
