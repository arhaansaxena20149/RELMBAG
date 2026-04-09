import requests
import os
import sys

def test_connection():
    # Default to the production Render server
    USE_REMOTE = os.environ.get("RELMBAG_REMOTE", "true").lower() == "true"
    SERVER_URL = os.environ.get("RELMBAG_SERVER_URL", "https://relmbag-server.onrender.com" if USE_REMOTE else "http://localhost:5050")
    
    print(f"Testing connection to: {SERVER_URL}")
    print(f"Mode: {'REMOTE' if USE_REMOTE else 'LOCAL'}")
    print("-" * 30)

    try:
        # 1. Test basic reachability (GET /)
        print(f"1. Testing reachability (GET {SERVER_URL}/)...")
        response = requests.get(SERVER_URL, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Content: {response.text}")
        
        if response.status_code == 200:
            print("   [SUCCESS] Server is reachable and running!")
        else:
            print("   [WARNING] Server is reachable but returned an error.")

        # 2. Test /debug (GET /debug)
        print(f"\n2. Testing /debug endpoint (GET {SERVER_URL}/debug)...")
        response = requests.get(f"{SERVER_URL}/debug", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Database Path: {data.get('database_path')}")
                print(f"   Tables: {', '.join(data.get('tables', []))}")
                print("   [SUCCESS] API endpoints are functioning correctly!")
            except:
                print("   [ERROR] /debug returned invalid JSON.")
        else:
            print("   [ERROR] /debug endpoint failed.")

    except requests.exceptions.ConnectionError as e:
        print(f"   [ERROR] Connection failed: {e}")
        print("\nPossible solutions:")
        print("1. Is the Render server up? Check dashboard.render.com.")
        print("2. Is the URL correct? (Current: https://relmbag-server.onrender.com)")
        print("3. Are you trying to test locally? Set RELMBAG_REMOTE=false.")
        print("4. Is the server still building on Render?")
    except requests.exceptions.Timeout:
        print("   [ERROR] Connection timed out. The server might be waking up or slow.")
    except Exception as e:
        print(f"   [ERROR] Unexpected error: {e}")

if __name__ == "__main__":
    test_connection()
