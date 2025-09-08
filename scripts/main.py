import flet as ft
from flet import *
from pages.home_page import HomePage
from pages.profile_page import ProfilePage
from pages.settings_page import SettingsPage

class AutoDeployApp:
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.setup_page()
        self.build_ui()

    def setup_page(self):
        self.page.title = "autoDeploy"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0d1117"
        self.page.window.width = 1400
        self.page.window.height = 900
        self.page.window.min_width = 700
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
            bgcolor=None,
            group_alignment=-0.2,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Home",
                    padding=ft.Padding(0,0,0,15)
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PERSON_OUTLINE,
                    selected_icon=ft.Icons.PERSON,
                    label="Profiles",
                    padding=ft.Padding(0,0,0,15)
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Settings",
                    padding=ft.Padding(0,0,0,15)
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INFO_OUTLINE,
                    selected_icon=ft.Icons.INFO,
                    label="About",
                    padding=ft.Padding(0,0,0,15)
                ),
            ],
            on_change=self.nav_change,
        )

        self.content_area = ft.Container(expand=True, padding=15, bgcolor="#0d1117")

        self.page.add(
            ft.Row([
                ft.Container(
                    bgcolor="#161b22",
                    alignment=ft.alignment.center,
                    border_radius=ft.BorderRadius(60, 20, 60, 20),
                    content=self.nav_rail
                ),
                ft.VerticalDivider(width=1, color="#21262d"),
                self.content_area,
            ], expand=True)
        )
                
        def route_change(e: ft.RouteChangeEvent):
            if self.page.route == "/":
                self.content_area.content = HomePage(self.page).content
            elif self.page.route == "/profile":
                self.content_area.content = ProfilePage(self.page).content
            elif self.page.route == "/settings":
                self.content_area.content = SettingsPage(self.page).content

            self.page.update()

        self.page.on_route_change = route_change
        self.page.go(self.page.route)

    def nav_change(self, e):
        selected = e.control.selected_index
        if selected == 0:
            self.content_area.content = HomePage(self.page).content
        elif selected == 1:
            self.content_area.content = ProfilePage(self.page).content
        elif selected == 2:
            self.content_area.content = SettingsPage(self.page).content
        elif selected == 3:
            print('============')
        
        self.page.update()
    
def main(page: ft.Page):
    AutoDeployApp(page)


if __name__ == "__main__":
    ft.app(target=main)