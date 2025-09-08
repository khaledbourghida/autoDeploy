from dataclasses import dataclass , asdict
from typing import Dict , Optional
import uuid
from datetime import datetime

@dataclass
class DeploymentProfile:
    id : str
    project_name : str
    type : str
    created_at : datetime
    status : str = 'pending'
    completed_at : datetime = None
    duration_seconds : int = 0
    
    @classmethod
    def create_deployment(cls , project_name : str , type : str ) -> 'DeploymentProfile':
        return cls(
            id = str(uuid.uuid4()),
            project_name = project_name,
            type = type,
            created_at = datetime.now(),
        )
    
    @classmethod
    def from_dict(cls , data : Dict) -> 'DeploymentProfile':
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        if data['completed_at']:
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        return cls(**data)
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        if self.completed_at :
            data['completed_at'] = self.completed_at.isoformat()
        return data