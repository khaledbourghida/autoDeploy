import flet as ft
from datetime import datetime
from storage.profile_store import ProfileStore
from models.github import GithubProfile


class CreateProfilePage:
    def __init__(self, app):
        self.app = app

    def build(self):
        platform_label = self.app.get_platform_label(self.app.current_platform_id)
        
        username_field = ft.TextField(
            label="GitHub Username",
            hint_text="Enter your GitHub username",
            bgcolor="#161b22",
            border_color="#21262d",
            focused_border_color="#238636"
        )
        
        email_field = ft.TextField(
            label="GitHub Email",
            hint_text="Enter your GitHub email address",
            bgcolor="#161b22",
            border_color="#21262d",
            focused_border_color="#238636"
        )
        
        token_field = ft.TextField(
            label="GitHub Personal Access Token",
            hint_text="Enter your GitHub PAT (with repo permissions)",
            password=True,
            can_reveal_password=True,
            bgcolor="#161b22",
            border_color="#21262d",
            focused_border_color="#238636"
        )

        def save_profile(e):
            username = username_field.value.strip() if username_field.value else ""
            email = email_field.value.strip() if email_field.value else ""
            token = token_field.value.strip() if token_field.value else ""
            
            if not username or not email or not token:
                self.app.show_dialog("Missing Fields", "Username, email, and token are required.")
                return
            
            try:
                profile = GithubProfile.create_profile(username, email, token)
                ProfileStore.save_profile(self.app.current_platform_id, profile.to_dict())
                self.app.show_dialog("Success", f"GitHub profile for '{username}' saved successfully.")
                self.app.open_platform(self.app.current_platform_id)
            except Exception as ex:
                self.app.show_dialog("Error", f"Failed to create profile: {str(ex)}")

        return ft.Column([
            ft.Row([
                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda e: self.app.show_home(),
                    tooltip="Back to Home"
                ),
                ft.Text("Create GitHub Profile", size=28, weight=ft.FontWeight.W_500, color="#f0f6fc"),
            ]),
            ft.Text(f"Platform: {platform_label}", size=16, color="#8b949e"),
            ft.Container(height=24),
            ft.Container(
                content=ft.Column([
                    ft.Text("GitHub Profile Information", size=18, weight=ft.FontWeight.W_500, color="#f0f6fc"),
                    ft.Container(height=8),
                    username_field,
                    email_field,
                    token_field,
                    ft.Container(height=16),
                    ft.Text(
                        "Note: Your GitHub token should have 'repo' permissions for full functionality.",
                        size=12,
                        color="#8b949e",
                        italic=True
                    ),
                    ft.Container(height=24),
                    ft.Row([
                        ft.ElevatedButton(
                            "Save Profile",
                            icon=ft.Icons.SAVE,
                            on_click=save_profile,
                            bgcolor="#238636",
                            color="#ffffff"
                        ),
                        ft.OutlinedButton(
                            "Cancel",
                            on_click=lambda e: self.app.show_home()
                        ),
                    ], spacing=12),
                ], spacing=16),
                padding=24,
                bgcolor="#161b22",
                border_radius=12,
                width=500,
            )
        ])
