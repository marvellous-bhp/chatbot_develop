import uuid

def create_input_data(session_id, chat_input):
    input_data = [
        {
            "sessionId": session_id,
            "action": "sendMessage",
            "chatInput": chat_input
        }
    ]
    return input_data

def generate_random_id():
    random_id = uuid.uuid4()
    return str(random_id)