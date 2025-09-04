import flet as ft


class NoProfilesPage:
    def __init__(self, app):
        self.app = app

    def build(self):
        platform_label = self.app.get_platform_label(self.app.current_platform_id)
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PERSON_OFF, size=64, color="#6e7681"),
                    ft.Text(
                        f"No {platform_label} profiles yet",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#f0f6fc"
                    ),
                    ft.Text(
                        f"You need at least one {platform_label} profile before deploying.\nCreate one to continue.",
                        size=14,
                        color="#8b949e",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=24),
                    ft.Row([
                        ft.ElevatedButton(
                            "Create Profile",
                            icon=ft.Icons.ADD,
                            on_click=lambda e: self.app.show_create_profile(),
                            bgcolor="#238636",
                            color="#ffffff"
                        ),
                        ft.OutlinedButton(
                            "Back to Home",
                            on_click=lambda e: self.app.show_home()
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16),
                padding=48,
                bgcolor="#161b22",
                border_radius=12,
                alignment=ft.alignment.center,
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
