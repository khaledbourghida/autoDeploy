import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from typing import List , Dict , Any 
from datetime import datetime
import requests
from utils.logger import get_logger , setup_logger
import json

class RateLimiter:
    def __init__(self , token : str):
        self.token = token
        setup_logger()
        self.logger = get_logger(__name__)
        data = self.get_rate_limit_status()
        self.update_rate_limit_info(data)

    def can_make_request(self) -> bool:
        try :
            self.logger.debug('Cheking if can make requests')
            with open('data/rate_limit.json' , 'r') as f :
                data = json.load(f)
            if data['resources']['core']['remaining'] <= 5 :
                self.logger.warn('Cant make request now , try again later')
                return False
            else :
                self.logger.info('You can make requests now')
                return True
        except Exception as e :
            self.logger.error('Exception error happen when check if can make requests')
            return False

    def update_rate_limit_info(self, data: Dict[str, Any]):
        self.logger.debug('updating rate limit info')
        with open('data/rate_limit.json' , 'w') as f :
            json.dump(data , f , indent=4)
        self.logger.info('rate limit info updated successfully')

    def get_rate_limit_status(self) -> Dict[str, Any]:
        try :
            self.logger.debug('Getting rate limit status')
            url = 'https://api.github.com/rate_limit'
            response = requests.get(url , headers = {
                'Authorization' : f'Bearer {self.token}',
                'Accept' : 'application/vnd.github+json'
            })
            data = response.json()
            self.logger.info('rate limit status fetched successfully')
            return data
        except Exception as e:
            self.logger.error('Exception error happen when get rate limit status')
            raise Exception('Cant get rate limit status')

    def get_reset_time(self) -> datetime:
        self.logger.debug('getting reset time')
        with open('data/rate_limit.json' , 'r') as f:
            data = json.load(f)
        reset_time = data['resources']['core']['reset']
        parsed_reset_time = datetime.fromtimestamp(reset_time)
        self.logger.info('reset time fetched successfully')
        return parsed_reset_time

    def get_remaining_requests(self) -> int:
        self.logger.debug('getting remaining requests')
        with open('data/rate_limit.json' , 'r') as f :
            data = json.load(f)
        self.logger.info('remaining requests fetched successfully')
        return data['resources']['core']['remaining']
