from dataclasses import dataclass , asdict
from typing import Dict , Optional
import uuid
from datetime import datetime

@dataclass
class GithubProfile:
    id : str
    username : str  #github username
    email : str     #github email
    github_token : str
    created_at : datetime
    last_used : datetime
    avatar_url : Optional[str] = None
    total_deployments : Optional[int] = 0
    successful_deployments : Optional[int] = 0
    failed_deployments : Optional[int] = 0
    pending_deployments : Optional[int] = 0

    @classmethod
    def create_profile(cls , username : str , email : str , github_token : str) -> 'GithubProfile':
        return cls(
            id = str(uuid.uuid4()),
            username = username,
            email = email,
            github_token = github_token,
            created_at = datetime.now(),
            last_used = datetime.now()
        )

    @classmethod
    def from_dict(cls , data : Dict) -> 'GithubProfile' :
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_used'] = datetime.fromisoformat(data['last_used'])
        return cls(**data)
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_used'] = self.last_used.isoformat()
        return data
