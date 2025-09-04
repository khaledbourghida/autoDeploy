"""
autoDeploy — Flet UI
Modern desktop app for multi-platform deployment management
Built with Flet for a professional, modern interface
"""

import flet as ft
from pages.home_page import HomePage
from pages.profiles_page import ProfilesPage
from pages.settings_page import SettingsPage
from pages.about_page import AboutPage
from pages.no_profiles_page import NoProfilesPage
from pages.platform_detail_page import PlatformDetailPage
from pages.create_profile_page import CreateProfilePage
from data.profile_store import ProfileStore


class AutoDeployApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_platform_id = "github"
        
        # Platform registry with comprehensive features
        self.platforms = [
            {"id": "github", "label": "GitHub", "icon": ft.Icons.CODE, "color": "#238636"},
            {"id": "netlify", "label": "Netlify", "icon": ft.Icons.CLOUD_UPLOAD, "color": "#00c7b7"},
            {"id": "render", "label": "Render", "icon": ft.Icons.STORAGE, "color": "#46e3b7"},
        ]
        
        # Comprehensive platform features
        self.features_map = {
            "github": [
                {"id": "create_repo", "label": "Create Repository", "icon": ft.Icons.CREATE_NEW_FOLDER, "desc": "Create a new GitHub repository"},
                {"id": "enable_pages", "label": "GitHub Pages", "icon": ft.Icons.WEB, "desc": "Deploy static site with GitHub Pages"},
                {"id": "create_release", "label": "Create Release", "icon": ft.Icons.ROCKET_LAUNCH, "desc": "Create and publish a new release"},
                {"id": "manage_actions", "label": "GitHub Actions", "icon": ft.Icons.PLAY_CIRCLE, "desc": "Setup CI/CD workflows"},
                {"id": "manage_webhooks", "label": "Webhooks", "icon": ft.Icons.WEBHOOK, "desc": "Configure repository webhooks"},
                {"id": "manage_secrets", "label": "Secrets", "icon": ft.Icons.LOCK, "desc": "Manage repository secrets"},
                {"id": "clone_repo", "label": "Clone Repository", "icon": ft.Icons.DOWNLOAD, "desc": "Clone existing repository"},
                {"id": "fork_repo", "label": "Fork Repository", "icon": ft.Icons.FORK_RIGHT, "desc": "Fork an existing repository"},
            ],
            "netlify": [
                {"id": "deploy_site", "label": "Deploy Site", "icon": ft.Icons.CLOUD_UPLOAD, "desc": "Deploy your site to Netlify"},
                {"id": "manage_domains", "label": "Custom Domains", "icon": ft.Icons.DOMAIN, "desc": "Configure custom domains"},
                {"id": "setup_forms", "label": "Forms", "icon": ft.Icons.SELECT_ALL, "desc": "Setup Netlify Forms"},
                {"id": "manage_functions", "label": "Functions", "icon": ft.Icons.FUNCTIONS, "desc": "Deploy serverless functions"},
                {"id": "setup_redirects", "label": "Redirects", "icon": ft.Icons.MOVE_UP, "desc": "Configure URL redirects"},
                {"id": "manage_env", "label": "Environment Variables", "icon": ft.Icons.SETTINGS, "desc": "Manage environment variables"},
                {"id": "setup_analytics", "label": "Analytics", "icon": ft.Icons.ANALYTICS, "desc": "Setup Netlify Analytics"},
                {"id": "manage_builds", "label": "Build Settings", "icon": ft.Icons.BUILD, "desc": "Configure build settings"},
            ],
            "render": [
                {"id": "deploy_web", "label": "Web Service", "icon": ft.Icons.WEB, "desc": "Deploy web applications"},
                {"id": "deploy_static", "label": "Static Site", "icon": ft.Icons.ANALYTICS, "desc": "Deploy static websites"},
                {"id": "setup_database", "label": "Database", "icon": ft.Icons.STORAGE, "desc": "Setup PostgreSQL database"},
                {"id": "setup_redis", "label": "Redis", "icon": ft.Icons.MEMORY, "desc": "Setup Redis instance"},
                {"id": "manage_cron", "label": "Cron Jobs", "icon": ft.Icons.SCHEDULE, "desc": "Schedule background jobs"},
                {"id": "manage_env", "label": "Environment Variables", "icon": ft.Icons.SETTINGS, "desc": "Manage environment variables"},
                {"id": "setup_domains", "label": "Custom Domains", "icon": ft.Icons.DOMAIN, "desc": "Configure custom domains"},
                {"id": "manage_scaling", "label": "Auto Scaling", "icon": ft.Icons.TRENDING_UP, "desc": "Configure auto scaling"},
            ],
        }
        
        self.setup_page()
        self.build_ui()

    def setup_page(self):
        self.page.title = "autoDeploy"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0d1117"
        self.page.window_width = 1400
        self.page.window_height = 900
        self.page.window_min_width = 1000
        self.page.window_min_height = 700
        
        # Custom theme colors
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#238636",
                on_primary="#ffffff",
                secondary="#21262d",
                surface="#161b22",
                on_surface="#f0f6fc",
                background="#0d1117",
                on_background="#f0f6fc",
            )
        )

    def build_ui(self):
        # Navigation rail
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            bgcolor="#161b22",
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Home"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PERSON_OUTLINE,
                    selected_icon=ft.Icons.PERSON,
                    label="Profiles"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Settings"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INFO_OUTLINE,
                    selected_icon=ft.Icons.INFO,
                    label="About"
                ),
            ],
            on_change=self.nav_change,
        )
        
        # Main content area
        self.content_area = ft.Container(
            content=HomePage(self).build(),
            expand=True,
            padding=24,
            bgcolor="#0d1117"
        )
        
        # Main layout
        self.page.add(
            ft.Row([
                self.nav_rail,
                ft.VerticalDivider(width=1, color="#21262d"),
                self.content_area,
            ], expand=True)
        )

    def nav_change(self, e):
        selected = e.control.selected_index
        if selected == 0:
            self.show_home()
        elif selected == 1:
            self.show_profiles()
        elif selected == 2:
            self.show_settings()
        elif selected == 3:
            self.show_about()

    def show_home(self):
        self.content_area.content = HomePage(self).build()
        self.page.update()

    def show_profiles(self):
        self.content_area.content = ProfilesPage(self).build()
        self.page.update()

    def show_settings(self):
        self.content_area.content = SettingsPage(self).build()
        self.page.update()

    def show_about(self):
        self.content_area.content = AboutPage(self).build()
        self.page.update()

    def open_platform(self, platform_id: str):
        self.current_platform_id = platform_id
        
        if not ProfileStore.has_profiles(platform_id):
            self.show_no_profiles()
        else:
            self.show_platform_detail()

    def show_no_profiles(self):
        self.content_area.content = NoProfilesPage(self).build()
        self.page.update()

    def show_platform_detail(self):
        self.content_area.content = PlatformDetailPage(self).build()
        self.page.update()

    def show_create_profile(self):
        self.content_area.content = CreateProfilePage(self).build()
        self.page.update()

    def handle_action(self, action):
        platform_label = self.get_platform_label(self.current_platform_id)
        self.show_dialog(
            action["label"],
            f"Selected action: {action['label']}\n\n"
            f"Platform: {platform_label}\n"
            f"Action ID: {action['id']}\n\n"
            f"Hook this to your API implementation."
        )

    def show_dialog(self, title: str, message: str):
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Close", on_click=close_dialog),
            ],
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def get_platform_label(self, platform_id: str) -> str:
        for p in self.platforms:
            if p["id"] == platform_id:
                return p["label"]
        return platform_id


def main(page: ft.Page):
    AutoDeployApp(page)


if __name__ == "__main__":
    ft.app(target=main)
