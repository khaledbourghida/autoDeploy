import json
import os
from typing import List, Dict


class ProfileStore:
    ROOT = os.path.join("data", "profiles")

    @classmethod
    def _file_for(cls, platform_id: str) -> str:
        os.makedirs(cls.ROOT, exist_ok=True)
        return os.path.join(cls.ROOT, f"{platform_id}.json")

    @classmethod
    def ensure_file(cls, platform_id: str) -> None:
        path = cls._file_for(platform_id)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"profiles": [], "projects": []}, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_profiles(cls, platform_id: str) -> List[Dict]:
        cls.ensure_file(platform_id)
        with open(cls._file_for(platform_id), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("profiles", [])

    @classmethod
    def load_projects(cls, platform_id: str) -> List[Dict]:
        cls.ensure_file(platform_id)
        with open(cls._file_for(platform_id), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("projects", [])

    @classmethod
    def has_profiles(cls, platform_id: str) -> bool:
        try:
            return len(cls.load_profiles(platform_id)) > 0
        except Exception:
            return False

    @classmethod
    def save_profile(cls, platform_id: str, profile: Dict) -> None:
        cls.ensure_file(platform_id)
        path = cls._file_for(platform_id)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f) or {"profiles": [], "projects": []}
        data.setdefault("profiles", []).append(profile)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def save_project(cls, platform_id: str, project: Dict) -> None:
        cls.ensure_file(platform_id)
        path = cls._file_for(platform_id)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f) or {"profiles": [], "projects": []}
        data.setdefault("projects", []).append(project)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def get_analytics(cls) -> Dict:
        """Get analytics data for all platforms"""
        analytics = {
            "total_projects": 0,
            "total_profiles": 0,
            "platforms": {}
        }
        
        platforms = ["github", "netlify", "render"]
        
        for platform in platforms:
            try:
                profiles = cls.load_profiles(platform)
                projects = cls.load_projects(platform)
                
                analytics["platforms"][platform] = {
                    "profiles": len(profiles),
                    "projects": len(projects)
                }
                
                analytics["total_profiles"] += len(profiles)
                analytics["total_projects"] += len(projects)
            except Exception:
                analytics["platforms"][platform] = {
                    "profiles": 0,
                    "projects": 0
                }
        
        return analytics
