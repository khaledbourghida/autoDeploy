import flet as ft


class AboutPage:
    def __init__(self, app):
        self.app = app

    def build(self):
        return ft.Column([
            ft.Text("About autoDeploy", size=28, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
            ft.Container(height=24),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ROCKET_LAUNCH, size=64, color="#238636"),
                        ft.Container(height=16),
                        ft.Text(
                            "autoDeploy v1.0.0",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#f0f6fc"
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Desktop automation UI for multi-platform deployments.",
                            size=16,
                            color="#8b949e",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=16),
                        ft.Text("Built with Flet for modern, professional interface.", color="#8b949e"),
                        ft.Container(height=24),
                        ft.Row([
                            ft.ElevatedButton(
                                "GitHub Repository",
                                icon=ft.Icons.CODE,
                                bgcolor="#21262d",
                                color="#f0f6fc"
                            ),
                            ft.ElevatedButton(
                                "Documentation",
                                icon=ft.Icons.BOOK,
                                bgcolor="#0969da",
                                color="#ffffff"
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40,
                    bgcolor="#161b22",
                    border_radius=12,
                ),
                elevation=2,
            ),
        ])
