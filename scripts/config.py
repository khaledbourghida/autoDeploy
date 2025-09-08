APP_CONFIG = {
    "name": "autoDeploy",
    "version": "1.0.0",
    "description": "Multi-platform deployment management",
    "platforms" : ['github' , 'netlify' , 'render'],
    "window": {
        "width": 1400,
        "height": 900,
        "min_width": 1000,
        "min_height": 700
    }
}

PLATFORM_ENDPOINTS = {
    "github": "https://api.github.com",
    "netlify": "https://api.netlify.com/api/v1",
    "render": "https://api.render.com/v1"
}
