from fastapi.testclient import TestClient
from src.server.app import app

client = TestClient(app)

print("Test 1: Empty body (none)")
response = client.post("/reset")
print("Status:", response.status_code)
print("Data:", response.json())

print("\nTest 2: null body string")
response = client.post("/reset", content="null", headers={"Content-Type": "application/json"})
print("Status:", response.status_code)
print("Data:", response.json())
