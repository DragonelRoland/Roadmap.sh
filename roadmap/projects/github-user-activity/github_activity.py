import sys
import urllib.request
import json

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        return data
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}")
        return None

def display_activity(activity):
    # TODO: Implement activity display logic
    pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python github_activity.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    activity = fetch_github_activity(username)

    if activity:
        display_activity(activity)

if __name__ == "__main__":
    main()
