import json

class RateLimitStorage:

    def get_reset_time(self) -> int:
        with open('data/rate_limit.json' , 'r') as f:
            data = json.load(f)
        return data['resources']['core']['reset'] | 0
        