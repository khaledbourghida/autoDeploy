import requests
import json
from typing import Dict, List, Optional
from data.profile_store import ProfileStore


class RenderAPI:
    BASE_URL = "https://api.render.com/v1"
    
    def __init__(self, profile_name: str):
        """Initialize with a specific Render profile"""
        profiles = ProfileStore.load_profiles("render")
        self.profile = next((p for p in profiles if p["name"] == profile_name), None)
        if not self.profile:
            raise ValueError(f"Profile '{profile_name}' not found")
        
        self.headers = {
            "Authorization": f"Bearer {self.profile['token']}",
            "Content-Type": "application/json"
        }
    
    def deploy_web_service(self, name: str, repo_url: str, build_command: str = "npm install", 
                          start_command: str = "npm start") -> Dict:
        """Deploy a web service"""
        data = {
            "type": "web_service",
            "name": name,
            "repo": repo_url,
            "buildCommand": build_command,
            "startCommand": start_command,
            "plan": "free"
        }
        
        url = f"{self.BASE_URL}/services"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def deploy_static_site(self, name: str, repo_url: str, build_command: str = "npm run build", 
                          publish_directory: str = "dist") -> Dict:
        """Deploy a static site"""
        data = {
            "type": "static_site",
            "name": name,
            "repo": repo_url,
            "buildCommand": build_command,
            "publishPath": publish_directory
        }
        
        url = f"{self.BASE_URL}/services"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def create_database(self, name: str, database_user: str, database_name: str) -> Dict:
        """Create a PostgreSQL database"""
        data = {
            "type": "postgresql",
            "name": name,
            "databaseUser": database_user,
            "databaseName": database_name,
            "plan": "free"
        }
        
        url = f"{self.BASE_URL}/services"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def create_redis(self, name: str, plan: str = "free") -> Dict:
        """Create a Redis instance"""
        data = {
            "type": "redis",
            "name": name,
            "plan": plan
        }
        
        url = f"{self.BASE_URL}/services"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def create_cron_job(self, name: str, command: str, schedule: str) -> Dict:
        """Create a cron job"""
        data = {
            "type": "cron_job",
            "name": name,
            "command": command,
            "schedule": schedule
        }
        
        url = f"{self.BASE_URL}/services"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def set_environment_variable(self, service_id: str, key: str, value: str) -> Dict:
        """Set environment variable for a service"""
        data = {
            "key": key,
            "value": value
        }
        
        url = f"{self.BASE_URL}/services/{service_id}/env-vars"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def setup_custom_domain(self, service_id: str, domain: str) -> Dict:
        """Setup custom domain"""
        data = {"name": domain}
        
        url = f"{self.BASE_URL}/services/{service_id}/custom-domains"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def configure_auto_scaling(self, service_id: str, min_instances: int = 1, 
                             max_instances: int = 3) -> Dict:
        """Configure auto scaling"""
        data = {
            "autoscaling": {
                "enabled": True,
                "min": min_instances,
                "max": max_instances
            }
        }
        
        url = f"{self.BASE_URL}/services/{service_id}"
        response = requests.patch(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def list_services(self) -> List[Dict]:
        """List all services"""
        url = f"{self.BASE_URL}/services"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return []
    
    def _handle_response(self, response: requests.Response) -> Dict:
        """Handle API response"""
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {
                "error": f"API Error {response.status_code}",
                "message": response.text
            }
