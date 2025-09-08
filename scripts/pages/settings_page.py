import flet as ft

class SettingsPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content = self.build_ui()
    def build_ui(self):
        return ft.Column(
            controls=[
                ft.Text("⚙️ Settings Page", size=24, weight="bold"),
                ft.Text("App preferences and configuration."),
            ]
        )