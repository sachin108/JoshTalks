import requests

create_user_url = 'http://127.0.0.1:8000/users/create/'
user_data = {
    "username": "joeX",
    "email": "joe@example.com",
    "password": "password123"
}
response = requests.post(create_user_url, json=user_data)
user_response = response.json()
print("User creation response:", user_response)
user_id = user_response['user']['id']  # Extract the user ID
print("--------*******-----------")

create_task_url = 'http://127.0.0.1:8000/tasks/create/'
task_data = {
    "name": "Task 1",
    "description": "This is a description of Task 1",
    "task_type": "development"
}
response = requests.post(create_task_url, json=task_data)
task_response = response.json()
print("Task creation response:", task_response)
task_id = task_response['task']['id']  # Extract the task ID
print("--------*******-----------")

assign_task_url = f'http://127.0.0.1:8000/tasks/{task_id}/assign/'
assign_data = {
    "user_ids": [user_id]
}
response = requests.post(assign_task_url, json=assign_data)
print("Task assignment response:", response.json())
