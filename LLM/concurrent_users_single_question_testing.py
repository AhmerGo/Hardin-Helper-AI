import concurrent.futures
import requests
import time
import random
import string
import statistics  # For calculating average and median
from tqdm import tqdm  # Import tqdm for the progress bar

# The endpoint where your chatbot listens for incoming messages
CHATBOT_ENDPOINT = 'http://localhost:3000/chat'

# Sample question to be sent by each user
SAMPLE_QUESTION = "hello"

# Number of simulated users
NUM_SIMULATED_USERS = 2 # Adjust this number based on your testing needs


# Function to generate a random ID of specified length
def generate_random_id(length=7):
    # Generate a random string of letters and digits
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# Function to simulate a single request from a user
def simulate_user_request(user_id):
    start_time = time.time()  # Start timing

    payload = {
        'user_input': SAMPLE_QUESTION,
        'session_id': user_id  # Unique user/session ID, now shorter
    }
    response_data = {}
    try:
        response = requests.post(CHATBOT_ENDPOINT, json=payload)
        response_data = response.json()
    except Exception as e:
        response_data = {'error': str(e)}

    duration = time.time() - start_time  # Calculate the duration
    return user_id, response_data, duration  # Return the user_id, response data, and duration


# Generate unique, shorter user IDs
user_ids = [generate_random_id() for _ in range(NUM_SIMULATED_USERS)]

# Set up a tqdm progress bar
progress_bar = tqdm(total=NUM_SIMULATED_USERS, desc="Processing user requests")

# Use ThreadPoolExecutor to simulate multiple users simultaneously
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_SIMULATED_USERS) as executor:
    # Submit all the tasks and create a list to hold the futures
    futures = [executor.submit(simulate_user_request, user_id) for user_id in user_ids]

    # As each future completes, update the progress bar and store results
    for future in concurrent.futures.as_completed(futures):
        user_id, response_data, duration = future.result()
        results.append((user_id, response_data, duration))
        progress_bar.update(1)  # Update the progress for each completed future

progress_bar.close()  # Close the progress bar

# Extract durations for statistical calculation
durations = [result[2] for result in results]

# Calculate statistics now that all requests have been processed
average_duration = statistics.mean(durations)
median_duration = statistics.median(durations)
max_duration = max(durations)
min_duration = min(durations)

# Printing the statistical results and responses
print(f"\nTotal processed requests: {len(results)}")
for user_id, response, duration in results:
    print(f"User {user_id} got response {response} in {duration:.2f} seconds")
print(f"Average response time: {average_duration:.2f} seconds")
print(f"Median response time: {median_duration:.2f} seconds")
print(f"Max response time: {max_duration:.2f} seconds")
print(f"Min response time: {min_duration:.2f} seconds")
