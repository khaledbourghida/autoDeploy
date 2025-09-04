# autoDeploy - Multi-Platform Deployment Manager

A modern desktop application built with Flet for managing deployments across multiple platforms including GitHub, Netlify, and Render.

## Project Structure

\`\`\`
scripts/
├── main_flet.py              # Main application entry point
├── config.py                 # Application configuration
├── requirements_flet.txt     # Python dependencies
├── data/
│   ├── __init__.py
│   └── profile_store.py      # Profile and project data management
├── pages/
│   ├── __init__.py
│   ├── home_page.py          # Home dashboard with analytics
│   ├── profiles_page.py      # Profile management
│   ├── settings_page.py      # Application settings
│   ├── about_page.py         # About information
│   ├── no_profiles_page.py   # No profiles state
│   ├── platform_detail_page.py  # Platform features
│   └── create_profile_page.py    # Profile creation
├── api/
│   ├── __init__.py
│   ├── github_api.py         # GitHub API integration
│   ├── netlify_api.py        # Netlify API integration
│   └── render_api.py         # Render API integration
└── utils/
    ├── __init__.py
    └── project_tracker.py    # Project tracking utilities
\`\`\`

## Features by Platform

### GitHub
- Create repositories
- Enable GitHub Pages
- Create releases
- Manage GitHub Actions
- Configure webhooks
- Manage secrets
- Clone/Fork repositories

### Netlify
- Deploy sites
- Custom domains
- Forms setup
- Serverless functions
- URL redirects
- Environment variables
- Analytics
- Build settings

### Render
- Web services
- Static sites
- PostgreSQL databases
- Redis instances
- Cron jobs
- Environment variables
- Custom domains
- Auto scaling

## Installation

1. Install dependencies:
\`\`\`bash
pip install -r requirements_flet.txt
\`\`\`

2. Run the application:
\`\`\`bash
python main_flet.py
\`\`\`

## Data Structure

The application stores data in `data/profiles/` with separate JSON files for each platform:
- `github.json` - GitHub profiles and projects
- `netlify.json` - Netlify profiles and projects  
- `render.json` - Render profiles and projects

Each file contains:
\`\`\`json
{
  "profiles": [
    {
      "name": "Profile Name",
      "token": "api_token",
      "owner": "optional_org",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "type": "web_service",
      "created_at": "2024-01-01T00:00:00Z",
      "status": "active"
    }
  ]
}
\`\`\`

## Usage

1. **Create Profiles**: Add API tokens for each platform
2. **Select Platform**: Choose GitHub, Netlify, or Render
3. **Execute Actions**: Use the feature cards to perform deployments
4. **Track Projects**: Monitor your deployments in the analytics dashboard

## API Integration

Each platform has its own API class in the `api/` directory. To use them:

\`\`\`python
from api.github_api import GitHubAPI

# Initialize with profile name
github = GitHubAPI("my-profile")

# Create repository
result = github.create_repository("my-new-repo", "Description", private=False)
\`\`\`

## Extending the Application

To add new platforms:
1. Create API class in `api/` directory
2. Add platform to `platforms` list in `main_flet.py`
3. Add features to `features_map`
4. Update `ProfileStore` to handle new platform data
