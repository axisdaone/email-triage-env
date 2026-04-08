# main.py
from fastapi import FastAPI
from models import Observation, Action, Reward, Email
from tasks import TASKS, grade_action
import copy

app = FastAPI()

# This is our in-memory "session state"
state_store = {
    "task_id": None,
    "emails": [],
    "current_index": 0,
    "step_count": 0,
    "total_reward": 0.0,
    "done": False,
}

@app.post("/reset")
def reset(task_id: str = "task1"):
    task = TASKS[task_id]
    state_store.update({
        "task_id": task_id,
        "emails": copy.deepcopy(task["emails"]),
        "current_index": 0,
        "step_count": 0,
        "total_reward": 0.0,
        "done": False,
    })
    first_email = state_store["emails"][0]
    return Observation(
        current_email=Email(**{k: first_email[k] for k in ["id","subject","sender","body","timestamp"]}),
        inbox_remaining=len(state_store["emails"]) - 1,
        step_count=0,
        task_id=task_id,
    )

@app.post("/step")
def step(action: Action):
    if state_store["done"]:
        return {"error": "Episode is done. Call /reset to start again."}

    emails = state_store["emails"]
    idx = state_store["current_index"]
    current_email = emails[idx]
    task_id = state_store["task_id"]

    # Grade the action
    reward_value = grade_action(task_id, current_email, action)
    state_store["total_reward"] += reward_value
    state_store["step_count"] += 1
    state_store["current_index"] += 1

    done = state_store["current_index"] >= len(emails)
    state_store["done"] = done

    reward = Reward(
        value=reward_value,
        reason=f"Label match + folder match score for email '{current_email['subject']}'"
    )

    if done:
        obs = Observation(
            current_email=Email(**{k: current_email[k] for k in ["id","subject","sender","body","timestamp"]}),
            inbox_remaining=0,
            step_count=state_store["step_count"],
            task_id=task_id,
        )
    else:
        next_email = emails[state_store["current_index"]]
        obs = Observation(
            current_email=Email(**{k: next_email[k] for k in ["id","subject","sender","body","timestamp"]}),
            inbox_remaining=len(emails) - state_store["current_index"] - 1,
            step_count=state_store["step_count"],
            task_id=task_id,
        )

    return {"observation": obs, "reward": reward, "done": done, "info": {"total_reward": state_store["total_reward"]}}

@app.get("/state")
def get_state():
    return state_store