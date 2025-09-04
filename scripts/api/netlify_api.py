import requests
import json
from typing import Dict, List, Optional
from storage.profile_store import ProfileStore


class NetlifyAPI:
    BASE_URL = "https://api.netlify.com/api/v1"
    
    def __init__(self, profile_name: str):
        """Initialize with a specific Netlify profile"""
        profiles = ProfileStore.load_profiles("netlify")
        self.profile = next((p for p in profiles if p["name"] == profile_name), None)
        if not self.profile:
            raise ValueError(f"Profile '{profile_name}' not found")
        
        self.headers = {
            "Authorization": f"Bearer {self.profile['token']}",
            "Content-Type": "application/json"
        }
    
    def deploy_site(self, site_name: str, build_command: str = "npm run build", 
                   publish_directory: str = "dist") -> Dict:
        """Deploy a new site to Netlify"""
        data = {
            "name": site_name,
            "build_settings": {
                "cmd": build_command,
                "dir": publish_directory
            }
        }
        
        url = f"{self.BASE_URL}/sites"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def setup_custom_domain(self, site_id: str, domain: str) -> Dict:
        """Setup custom domain for a site"""
        data = {"hostname": domain}
        
        url = f"{self.BASE_URL}/sites/{site_id}/domains"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def create_form(self, site_id: str, form_name: str, fields: List[str]) -> Dict:
        """Create a Netlify form"""
        data = {
            "name": form_name,
            "fields": [{"name": field, "type": "text"} for field in fields]
        }
        
        url = f"{self.BASE_URL}/sites/{site_id}/forms"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def deploy_function(self, site_id: str, function_name: str, function_code: str) -> Dict:
        """Deploy a serverless function"""
        # This is a simplified version - actual deployment would involve zip upload
        return {
            "message": f"Function '{function_name}' deployment prepared",
            "note": "Actual function deployment requires zip file upload"
        }
    
    def setup_redirect(self, site_id: str, from_path: str, to_path: str, 
                      status_code: int = 301) -> Dict:
        """Setup URL redirect"""
        data = {
            "from": from_path,
            "to": to_path,
            "status": status_code
        }
        
        url = f"{self.BASE_URL}/sites/{site_id}/redirects"
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def set_environment_variable(self, site_id: str, key: str, value: str) -> Dict:
        """Set environment variable"""
        data = {key: value}
        
        url = f"{self.BASE_URL}/sites/{site_id}/env"
        response = requests.patch(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def enable_analytics(self, site_id: str) -> Dict:
        """Enable Netlify Analytics"""
        url = f"{self.BASE_URL}/sites/{site_id}/analytics"
        response = requests.post(url, headers=self.headers)
        return self._handle_response(response)
    
    def update_build_settings(self, site_id: str, build_command: str, 
                             publish_directory: str, base_directory: str = "") -> Dict:
        """Update build settings"""
        data = {
            "build_settings": {
                "cmd": build_command,
                "dir": publish_directory,
                "base": base_directory
            }
        }
        
        url = f"{self.BASE_URL}/sites/{site_id}"
        response = requests.patch(url, headers=self.headers, json=data)
        return self._handle_response(response)
    
    def list_sites(self) -> List[Dict]:
        """List all sites"""
        url = f"{self.BASE_URL}/sites"
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
