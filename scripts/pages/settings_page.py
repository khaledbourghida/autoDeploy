import flet as ft


class SettingsPage:
    def __init__(self, app):
        self.app = app

    def build(self):
        return ft.Column([
            ft.Text("Settings", size=28, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
            ft.Container(height=24),
            
            # Theme settings
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Appearance", size=18, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
                        ft.Container(height=8),
                        ft.Row([
                            ft.Text("Theme Mode:", color="#8b949e"),
                            ft.Container(expand=True),
                            ft.Switch(value=True, label="Dark Mode", disabled=True),
                        ]),
                    ]),
                    padding=20,
                    bgcolor="#161b22",
                    border_radius=12,
                ),
                elevation=2,
            ),
            
            ft.Container(height=16),
            
            # API settings
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("API Configuration", size=18, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
                        ft.Container(height=8),
                        ft.Text("Configure API timeouts and retry settings", color="#8b949e"),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Text("Request Timeout:", color="#8b949e"),
                            ft.Container(expand=True),
                            ft.TextField(value="30", width=80, text_size=12),
                            ft.Text("seconds", color="#8b949e"),
                        ]),
                    ]),
                    padding=20,
                    bgcolor="#161b22",
                    border_radius=12,
                ),
                elevation=2,
            ),
        ])
