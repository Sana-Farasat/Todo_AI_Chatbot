import asyncio
import httpx

async def test_with_error():
    async with httpx.AsyncClient(timeout=30.0) as client:
        token = "eyJhbGciOiJFZERTQSIsImtpZCI6IkI0NXJMUVRjTFNZQUlvbWNhTFZtYmVOcFppTnZrZ3N1In0.eyJpYXQiOjE3NzE3MDExMDgsIm5hbWUiOiJUZXN0IFVzZXIgMiIsImVtYWlsIjoidGVzdDJAZGVtby5jb20iLCJlbWFpbFZlcmlmaWVkIjpmYWxzZSwiaW1hZ2UiOm51bGwsImNyZWF0ZWRBdCI6IjIwMjYtMDItMjFUMTk6MTE6NDcuMjE5WiIsInVwZGF0ZWRBdCI6IjIwMjYtMDItMjFUMTk6MTE6NDcuMjE5WiIsImlkIjoiQkZ6Q3pielVZMlpKaDE2YkZCWlA5ZmNZeDFIS3ZZVWsiLCJzdWIiOiJCRnpDemJ6VVkyWkpoMTZiRkJaUDlmY1l4MUhLdllVayIsImV4cCI6MTc3MTcwNDcwOCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDozMDAwIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDozMDAwIn0.9-TClaq1kC2McN9CaVdJNf5Kz0f7TSOFnsBYLXKVvC25JZ5-NuaNy8CGW4cd8f3f_pYCERhgp9lO0lly8dhtBQ"
        
        try:
            response = await client.post(
                "http://localhost:8000/api/BFzCzbzUY2ZJh16bFBZP9fcYx1HKvYUk/tasks/",
                json={"title": "Test Task"},
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            print(f"Headers: {dict(response.headers)}")
            
            # Try to get error detail
            if response.status_code == 500:
                print("\nServer error! Checking response content...")
                print(f"Content: {response.content}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {e.response.text}")
        except httpx.RequestError as e:
            print(f"Request Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {type(e).__name__}: {e}")

asyncio.run(test_with_error())
