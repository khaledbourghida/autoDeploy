from typing import Dict , List , Any , Optional
from utils.logger import setup_logger , get_logger
from config import PLATFORM_ENDPOINTS
import requests
from .github_ratelimit import RateLimiter

class GitHubService:
    def __init__(self , user_data : Dict):
        setup_logger()
        self.logger = get_logger(__name__)
        self.base_url = PLATFORM_ENDPOINTS['github']
        self.data = user_data
        rate_limit = RateLimiter(self.data['github_token'])
        reset_time = rate_limit.get_reset_time()
        can_make_req = rate_limit.can_make_request()
        if not can_make_req :
            raise Exception(f'Cant make request now , try again after : {reset_time}')

    # Repository Management:
    def create_repository(self, name: str, description: str = "", private: bool = False) -> str | Dict:
        try:
            self.logger.debug(f'Creating repo with name : {name}')
            url = f'{self.base_url }/user/repos'
            data = {
                'name' : name,
                'description' : description,
                'private' : private
            }
            response = requests.post(url , headers= {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json',
                'Content-Type': 'application/json',
            } , json = data)
            if response.status_code in [200 , 201] :
                self.logger.info('Repo created successfully')
                repo_data = response.json()
                return repo_data.get('html_url', f'{self.base_url}/{self.data["username"]}/{name}.git')
            else :
                self.logger.warn('API error happen when create repo')
                return {
                    "error": f"API Error {response.status_code}",
                    "message": response.text
                }
        except Exception as e :
            self.logger.error('Execption error happen when create repo')
            raise Exception('Cant create a new repo , try again later')

    def get_repository(self, name: str) -> Optional[Dict[str, Any]]:
        try :
            self.logger.debug(f'Getting the repo with name : {name}')
            url = f'{self.base_url}/repos/{self.data['username']}/{name}'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201]:
                self.logger.info('Got the repo successfully')
                return response.json()
            else :
                self.logger.warn('API error happen when get the repo')
                return {
                    "error": f"API Error {response.status_code}",
                    "message": response.text
                }
        except Exception as e :
            self.logger.error('Execption error happen when get the repo')
            raise Exception('Cant get the repo , try again later')

    def delete_repository(self, name: str) -> bool:
        try :
            self.logger.debug(f'Deleting the repo with name : {name}')
            url = f'{self.base_url}/repos/{self.data['username']}/{name}'
            response = requests.delete(url , headers= {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('Deleted repo successfully')
                return True
            else :
                self.logger.warn('API error happen when delete the repo')
                return False
        except Exception as e:
            self.logger.error('Exception error happen when delete the repo')
            raise Exception('Cant delete the repo , try again later')

    def list_repositories(self) -> Dict[str, Any]:
        try :
            self.logger.debug('Getting list of repositories')
            url = f'{self.base_url}/user/repos'
            response = requests.get(url , headers= {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201]:
                self.logger.info('Got repositories successfully')
                return response.json()
            else :
                self.logger.warn('API error happen when get repositories')
                return {
                    "error": f"API Error {response.status_code}",
                    "message": response.text
                }
        except Exception as e:
            self.logger.error('Exception error happen when get repositories')
            raise Exception('Cant get repositories , try again later ')

    def update_repository(self, name: str, updates: Dict[str, Any]) -> bool:
        try :
            self.logger.debug(f'Updating the repo with name : {name}')
            url = f'{self.base_url}/repos/{self.data['username']}/{name}'
            response = requests.post(url , headers= {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json',
                'Content-Type' : 'application/json'
            } , data=updates)
            if response.status_code in [200 , 201] :
                self.logger.info('Updated repo successfully')
                return True
            else:
                self.logger.warn('API error happen when update the repo')
                return False
        except Exception as e :
            self.logger.error('Exception error happen when update the repo ')
            raise Exception('Cant update the repo , try again later')

    # GitHub Pages:
    def enable_github_pages(self, repo_name: str, branch: str = "gh-pages", path: str = "/") -> Dict | Optional[str]:
        try :
            self.logger.debug('Enabling github pages')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/pages'
            response = requests.post(url , headers={
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json',
                'Content-Type' : 'application/json'
            } , data = 
                {
                    "source": {
                        "branch": branch,
                        "path":path
                    },
                    "build_type": "legacy"
                }
            )
            if response.status_code in [200 , 201] :
                self.logger.info('Enabled github page successfully')
                return f'https://{self.data['username']}.github.io/{repo_name}/'
            else : 
                self.logger.warn('API error happen when enable github page')
                return {
                    "error": f"API Error {response.status_code}",
                    "message": response.text
                }
        except Exception as e :
            self.logger.error('Exception error happen when enable github pages')
            raise Exception('Cant enable github pages now , try again later')

    def disable_github_pages(self, repo_name: str) -> bool:
        try :
            self.logger.debug('disabling github pages')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/pages'
            response = requests.delete(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('disabled github pages successfully')
                return True
            else : 
                self.logger.warn('API error happen when disable the github pages')
                return False
        except Exception as e :
            self.logger.error('Exception error happen when disable the github page')
            raise Exception('Cant disable the github pages now , try again later')

    def get_pages_info(self, repo_name: str) -> Optional[Dict[str, Any]]:
        try : 
            self.logger.debug('getting pages info')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/pages'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201] :
                self.logger.info('Got github page info successfully')
                return response.json()
            else :
                self.logger.warn('API error happen when get the info')
                return {
                    "error": f"API Error {response.status_code}",
                    "message": response.text
                }
        except Exception as e :
            self.logger.error('Exception error happen when get the info')
            raise Exception('Cant get the info about the page now , try again later')

    def update_pages_settings(self, repo_name: str, settings: Dict[str, Any]) -> bool:
        try :
            self.logger.debug('updating settings pages')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/pages'
            response = requests.put(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json',
                'Content-Type' : 'application/json'
            } , data = settings)
            if response.status_code in [200 , 201] :
                self.logger.info('Updated settings pages successfully')
                return True
            else :
                self.logger.warn('API error happen when update the settings pages')
                return {
                    'error' : f'API Error {response.status_code}',
                    'message' : response.text
                }
        except Exception as e :
            self.logger.error('Exception error Happen when update the settings pages')
            raise Exception('Cant update the settings page now , try again later')

    # User Management:
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        try : 
            self.logger.debug('Getting user info')
            url = f'{self.base_url}/user'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201] :
                self.logger.info('Fetched user info successfully')
                return response.json()
            else :
                self.logger.warn('API error happen when get the user info')
                return {
                    'error' : f'API Error {response.status_code}',
                    'message' : response.text
                }
        except Exception as e :
            self.logger.error('Exception error happen when get user info')
            raise Exception('Cant get user info now , try again later')

    def validate_token(self) -> bool:
        try : 
            self.logger.debug('validating token')
            url = f'{self.base_url}/user'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201] :
                self.logger.info('validated token successfully')
                return True
            else :
                self.logger.warn('API error happen when validate token')
                return False
        except Exception as e :
            self.logger.error('Exception error happen when validate token')
            raise Exception('Cant validate token now , try again later')

    def get_token_permissions(self) -> List[str]:
        try : 
            self.logger.debug('Getting token permission')
            url = f'{self.base_url}/user'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201] :
                self.logger.info('Fetched token permission successfully')
                return response.json()['X-OAuth-Scopes']
            else :
                self.logger.warn('API error happen when get token permission')
                return {
                    'error' : f'API Error {response.status_code}',
                    'message' : response.text
                }
        except Exception as e :
            self.logger.error('Exception error happen when get token permission')
            raise Exception('Cant get token permission now , try again later')

    def get_rate_limit_status(self) -> Dict[str, Any]:
        try :
            self.logger.debug('getting rate limit status')
            url = f'{self.base_url}/rate_limit'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201] :
                self.logger.info('Fetched rate limit status successfully')
                return response.json()
            else :
                self.logger.warn('API error happen when fetch rate limit status')
                return {
                    'error' : f'API Error {response.status_code}',
                    'message' : response.text
                }
        except Exception as e :
            self.logger.error('Exception error happen when get rate limit status')
            raise Exception('Cant get rate limit status now , try again later')

    # Collaborators:
    def add_collaborator(self, repo_name: str, username: str, permission: str = "push") -> bool:
        try :
            self.logger.debug('Adding collabprator')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/collaborators/{username}'
            response = requests.put(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json',
                'Content-Type' : 'application/json'
            } , data = {
                'permission' : permission
            })
            if response.status_code in [200 , 201] :
                self.logger.info('collaborator added successfully')
                return True
            elif response.status_code == 204 :
                self.logger.warn('user is already collaborator')
                return True
            else :
                self.logger.warn('API error happen when add collaborator')
                return False
        except Exception as e :
            self.logger.error('Exception error happen when add collaborator')
            raise Exception('Cant add collaborator now , try again later')

    def remove_collaborator(self, repo_name: str, username: str) -> bool:
        try :
            self.logger.debug('removing collbaorator')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/collaborators/{username}'
            response = requests.delete(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('collaborator removed successfully')
                return True
            else :
                self.logger.warn('API error happen when remove the collaborator')
                return False
        except Exception as e :
            self.logger.error('Exception error happen when remove collaborator')
            raise Exception('Cant remove collaborator now , try again later')

    def list_collaborators(self, repo_name: str) -> List[Dict[str, Any]] | Dict:
        try:
            self.logger.debug('fetching collaborators')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/collaborators'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('collaborators fetched successfully')
                return response.json()
            else :
                self.logger.warn('API error happen when get collaborators')
                return {
                    'error' : f'API Error {response.status_code}',
                    'message' : response.text
                }
        except Exception as e :
            self.logger.error('Exception error happen when get collaborators')
            raise Exception('Cant get collaborators now , try again later')

    # Releases:
    def create_release(self, repo_name: str, tag_name: str, name: str, body: str = "", draft: bool = False) -> Optional[Dict[str, Any]]:
        try:
            self.logger.debug('Creating release')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/releases'
            response = requests.post(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json',
                'Content-Type' : 'application/json'
            } , data = {
            "tag_name": tag_name,
            "target_commitish": "main",
            "name": name,
            "body": body,
            "draft": draft,
            "prerelease": False,
            "generate_release_notes": True
            }
        )
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('Release craeted successfully')
                return response.json()
            else :
                self.logger.warn('API error happen when create release')
                return {
                    'error' : f'API Error {response.status_code}',
                    'message' : response.text
                }
        except Exception as e :
            self.logger.error('Exception error happen when create release')
            raise Exception('Cant create release now , try again later')

    def list_releases(self, repo_name: str) -> List[Dict[str, Any]] | Dict:
        try :
            self.logger.debug('fetching releases')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/releases'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('Releases fetched successfully')
                return response.json()
            else :
                self.logger.warn('API error happen when get releases')
                return {
                    'error' : f'API Error {response.status_code}',
                    'message' : response.text
                }
        except Exception as e:
            self.logger.error('Exception error happen when get releases')
            raise Exception('Cant get releases now , try again later')

    def delete_release(self, repo_name: str, release_id: str) -> bool:
        try :
            self.logger.debug('deleting release')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/releases/{release_id}'
            response = requests.delete(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('release deleted successfully')
                return True
            else :
                self.logger.warn('API error happen when delete release')
                return False
        except Exception as e:
            self.logger.error('Exception eror happen when delete release')
            raise Exception('Cant delete release now , try again later')

    # Actions:
    def trigger_workflow(self, repo_name: str, workflow_id: str, ref: str = "main", inputs: Dict[str, Any] = None) -> bool:
        try :
            self.logger.debug('triggering workflow')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/actions/workflows/{workflow_id}/dispatches'
            response = requests.post(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json',
                'Content_Type' : 'application/json'
            } , data = {
                "ref" : ref,
                "inputs" : inputs
            })
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('workflow triggered successfully')
                return True
            else :
                self.logger.warn('API error happen when trigger workflow')
                return False
        except Exception as e:
            self.logger.error('Exception error happen when trigger workflow')
            raise Exception('Cant trigger workflow now , try again later')

    def get_workflow_runs(self, repo_name: str , workflow_id : str) -> List[Dict[str, Any]] | Dict:
        try :
            self.logger.debug('getting workflow runs')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/actions/workflows/{workflow_id}/runs'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('workflow runs fetched successfully')
                return response.json()
            else :
                self.logger.warn('API error happen when get workflow runs')
                return {
                    'error' : f'API Error {response.status_code}',
                    'message' : response.text
                }
        except Exception as e:
            self.logger.error('Exception error happen when get workflow runs')
            raise Exception('Cant get workflow runs now , try again later')  

    def cancel_workflow_run(self, repo_name: str, run_id: str) -> bool :
        try :
            self.logger.debug('canceling workflow run')
            url = f'{self.base_url}/repos/{self.data['username']}/{repo_name}/actions/runs/{run_id}/cancel'
            response = requests.post(url , headers = {
                'Authorization' : f'Bearer {self.data['github_token']}',
                'Accept' : 'application/vnd.github+json'
            })
            if response.status_code in [200 , 201 , 204] :
                self.logger.info('workflow run canceled successfully')
                return True
            else :
                self.logger.warn('API error happen when cancel workflow run')
                return False
        except Exception as e:
            self.logger.error('Exception error happen when cancel workflow run')
            raise Exception('Cant cancel workflow run now , try again later')