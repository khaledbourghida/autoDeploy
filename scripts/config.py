"""
Configuration file for autoDeploy application
"""

# Application settings
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

# Theme configuration
THEME_CONFIG = {
    "colors": {
        "github": "#238636",
        "netlify": "#00c7b7", 
        "render": "#46e3b7",
        "background": "#0d1117",
        "surface": "#161b22",
        "text_primary": "#f0f6fc",
        "text_secondary": "#8b949e"
    }
}

# Platform endpoints
PLATFORM_ENDPOINTS = {
    "github": "https://api.github.com",
    "netlify": "https://api.netlify.com/api/v1",
    "render": "https://api.render.com/v1"
}
