def create_user_schema(user_id, name, email):
    """
    Blueprint for the 'users' collection.
    Matches the JSON structure we designed.
    """
    return {
        "user_id": user_id,
        "name": name,
        "email": email,
        "created_at": "SERVER_TIMESTAMP",
        "preferences": {
            "voice_id": "default_voice",
            "dietary_restrictions": "None",
            "fitness_goals": "General Health"
        }
    }

def create_task_schema(task_id, user_id, agent_type, status="pending"):
    """
    Blueprint for the 'active_tasks' collection.
    """
    return {
        "task_id": task_id,
        "user_id": user_id,
        "agent_type": agent_type,
        "status": status,
        "current_step": "initiated",
        "data": {}
    }