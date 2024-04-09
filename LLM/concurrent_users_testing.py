import concurrent.futures
import requests
import uuid

# The endpoint where your chatbot listens for incoming messages
CHATBOT_ENDPOINT = 'http://localhost:5000/chat'

# Predefined sets of questions for variety in user sessions
QUESTION_SETS = [
    [
        "Hello, how are you?",
        "What is the weather today?",
        "Tell me a joke."
    ],
    [
        "What's the latest news?",
        "Can you give me a movie recommendation?",
        "What day is it today?"
    ],
    # Add more sets of questions as needed
]

# Number of simulated users
NUM_SIMULATED_USERS = 5  # Adjust this number based on your testing needs


# Function to simulate a user session by sending a series of messages
def simulate_user_session(session_id, messages):
    responses = []

    for message in messages:
        payload = {
            'user_input': message,
            'session_id': session_id  # Use the same session_id for all messages in the session
        }
        try:
            response = requests.post(CHATBOT_ENDPOINT, json=payload)
            responses.append(response.json())
        except Exception as e:
            responses.append({'error': str(e)})

    return responses


# Generate user sessions dynamically based on NUM_SIMULATED_USERS
user_sessions = [(str(uuid.uuid4()), QUESTION_SETS[i % len(QUESTION_SETS)]) for i in range(NUM_SIMULATED_USERS)]

# Using ThreadPoolExecutor to simulate multiple users simultaneously
with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_SIMULATED_USERS) as executor:
    # Submit each user session to the executor
    future_to_session = {executor.submit(simulate_user_session, session_id, messages): session_id for
                         session_id, messages in user_sessions}

    # Collect and print the results as they complete
    for future in concurrent.futures.as_completed(future_to_session):
        session_id = future_to_session[future]
        try:
            session_results = future.result()
            print(f"Results for Session {session_id}:")
            for result in session_results:
                print(result)
        except Exception as e:
            print(f"Session {session_id} generated an exception: {e}")
