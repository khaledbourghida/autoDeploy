from datetime import datetime
from typing import Dict, List
from storage.profile_store import ProfileStore


class ProjectTracker:
    """Track and manage deployment projects"""
    
    @staticmethod
    def create_project(platform_id: str, project_data: Dict) -> None:
        """Create a new project entry"""
        project = {
            **project_data,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "status": "active",
            "deployments": []
        }
        ProfileStore.save_project(platform_id, project)
    
    @staticmethod
    def add_deployment(platform_id: str, project_name: str, deployment_data: Dict) -> None:
        """Add a deployment record to a project"""
        # This would require updating the existing project
        # For now, just save as a new deployment entry
        deployment = {
            "project_name": project_name,
            "deployed_at": datetime.utcnow().isoformat() + "Z",
            **deployment_data
        }
        ProfileStore.save_project(platform_id, deployment)
    
    @staticmethod
    def get_project_stats(platform_id: str) -> Dict:
        """Get statistics for projects on a platform"""
        projects = ProfileStore.load_projects(platform_id)
        
        return {
            "total_projects": len(projects),
            "active_projects": len([p for p in projects if p.get("status") == "active"]),
            "recent_deployments": len([p for p in projects if "deployed_at" in p])
        }
