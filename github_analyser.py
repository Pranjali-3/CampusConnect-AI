import requests
import os

class GitHubAnalyzer:
    def __init__(self):
        # Feature 22: Uses GITHUB_TOKEN for high-speed API access
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {"Authorization": f"token {self.token}"} if self.token else {}

    def fetch_user_data(self, username):
        # Feature 1 & 26: Fetches data in under 2 minutes with error handling
        try:
            user_url = f"https://api.github.com/users/{username}"
            repo_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
            
            user_res = requests.get(user_url, headers=self.headers)
            repo_res = requests.get(repo_url, headers=self.headers)

            if user_res.status_code != 200: return None
            return {"profile": user_res.json(), "repos": repo_res.json()}
        except Exception:
            return None