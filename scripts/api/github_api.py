import requests
import json
from typing import Dict, List, Optional
from storage.profile_store import ProfileStore


class GitHubAPI:
    BASE_URL = "https://api.github.com"
    
    def __init__(self, profile_name: str):
        """Initialize with a specific GitHub profile"""
        profiles = ProfileStore.load_profiles("github")
        self.profile = next((p for p in profiles if p["name"] == profile_name), None)
        if not self.profile:
            raise ValueError(f"Profile '{profile_name}' not found")
        
        self.headers = {
            "Authorization": f"token {self.profile['token']}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "autoDeploy-App"
        }
    
    def create_repository(self, name: str, description: str = "", private: bool = False, 
                         auto_init: bool = True) -> Dict:
        """Create a new GitHub repository"""
        data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init,
            "gitignore_template": "Python"
        }
        
        # Use organization if specified in profile
        if self.profile.get("owner"):
            url = f"{self.BASE_URL}/orgs/{self.profile['owner']}/repos"
        else:
            url = f"{self.BASE_URL}/user/repos"
        
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def enable_github_pages(self, repo_name: str, source_branch: str = "main", 
                           source_path: str = "/") -> Dict:
        """Enable GitHub Pages for a repository"""
        owner = self.profile.get("owner") or self._get_authenticated_user()["login"]
        url = f"{self.BASE_URL}/repos/{owner}/{repo_name}/pages"
        
        data = {
            "source": {
                "branch": source_branch,
                "path": source_path
            }
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def create_release(self, repo_name: str, tag_name: str, name: str, 
                      body: str = "", draft: bool = False, prerelease: bool = False) -> Dict:
        """Create a new release"""
        owner = self.profile.get("owner") or self._get_authenticated_user()["login"]
        url = f"{self.BASE_URL}/repos/{owner}/{repo_name}/releases"
        
        data = {
            "tag_name": tag_name,
            "name": name,
            "body": body,
            "draft": draft,
            "prerelease": prerelease
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def create_webhook(self, repo_name: str, webhook_url: str, events: List[str] = None) -> Dict:
        """Create a webhook for the repository"""
        if events is None:
            events = ["push", "pull_request"]
        
        owner = self.profile.get("owner") or self._get_authenticated_user()["login"]
        url = f"{self.BASE_URL}/repos/{owner}/{repo_name}/hooks"
        
        data = {
            "name": "web",
            "active": True,
            "events": events,
            "config": {
                "url": webhook_url,
                "content_type": "json"
            }
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def create_secret(self, repo_name: str, secret_name: str, secret_value: str) -> Dict:
        """Create or update a repository secret"""
        owner = self.profile.get("owner") or self._get_authenticated_user()["login"]
        
        # First get the public key
        key_url = f"{self.BASE_URL}/repos/{owner}/{repo_name}/actions/secrets/public-key"
        key_response = requests.get(key_url, headers=self.headers)
        
        if key_response.status_code != 200:
            return {"error": "Failed to get public key"}
        
        # For simplicity, returning success without actual encryption
        # In production, you'd encrypt the secret with the public key
        return {"message": f"Secret '{secret_name}' would be created (encryption not implemented in demo)"}
    
    def fork_repository(self, owner: str, repo_name: str, organization: str = None) -> Dict:
        """Fork a repository"""
        url = f"{self.BASE_URL}/repos/{owner}/{repo_name}/forks"
        
        data = {}
        if organization:
            data["organization"] = organization
        
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def clone_repository(self, repo_url: str, local_path: str) -> Dict:
        """Clone a repository (returns git command to execute)"""
        return {
            "command": f"git clone {repo_url} {local_path}",
            "message": "Execute this command in your terminal to clone the repository"
        }
    
    def list_repositories(self) -> List[Dict]:
        """List user repositories"""
        url = f"{self.BASE_URL}/user/repos"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return []
    
    def _get_authenticated_user(self) -> Dict:
        """Get authenticated user info"""
        url = f"{self.BASE_URL}/user"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)
    
    def _handle_response(self, response: requests.Response) -> Dict:
        """Handle API response"""
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {
                "error": f"API Error {response.status_code}",
                "message": response.text
            }
