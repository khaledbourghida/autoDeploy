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
from pages.github_features_page import GitHubFeaturesPage
from pages.netlify_features_page import NetlifyFeaturesPage
from pages.render_features_page import RenderFeaturesPage
from pages.create_profile_page import CreateProfilePage
from storage.profile_store import ProfileStore
from config import APP_CONFIG

class AutoDeployApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_platform_id = "github"
        
        self.platforms = [
            {"id": "github", "label": "GitHub", "icon": ft.Icons.CODE, "color": "#238636"},
            {"id": "netlify", "label": "Netlify", "icon": ft.Icons.CLOUD_UPLOAD, "color": "#00c7b7"},
            {"id": "render", "label": "Render", "icon": ft.Icons.STORAGE, "color": "#46e3b7"},
        ]
        
        self.setup_page()
        self.build_ui()

    def setup_page(self):
        self.page.title = "autoDeploy"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0d1117"
        self.page.window.width = 1400
        self.page.window.height = 900
        self.page.window.min_width = 1000
        self.page.window.min_height = 700
        
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
            self.show_platform_features()

    def show_no_profiles(self):
        self.content_area.content = NoProfilesPage(self).build()
        self.page.update()

    def show_platform_features(self):
        if self.current_platform_id == "github":
            self.content_area.content = GitHubFeaturesPage(self).build()
        elif self.current_platform_id == "netlify":
            self.content_area.content = NetlifyFeaturesPage(self).build()
        elif self.current_platform_id == "render":
            self.content_area.content = RenderFeaturesPage(self).build()
        self.page.update()

    def show_create_profile(self):
        self.content_area.content = CreateProfilePage(self).build()
        self.page.update()

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
