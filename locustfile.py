from locust import HttpUser, between, task
import random

class GroupSelectionUser(HttpUser):
    wait_time = between(1, 3)  # Simulates wait time between requests (1 to 3 seconds)

    @task
    def select_group(self):
        # Simulate a student selecting a group
        student_id = f"student_{random.randint(1, 1000000000)}"  # Generate random student IDs for testing
        group_id = random.choice([1, 2])  # Assuming two groups with IDs 1 and 2

        # POST request to select a group
        self.client.post("/select", data={
            "student_id": student_id,
            "group": group_id
        })

    def on_start(self):
        # This method runs when a simulated user starts, used to initialize or prepare data
        print("Starting load test for group selection...")

