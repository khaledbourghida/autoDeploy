import flet as ft
from datetime import datetime
from storage.profile_store import ProfileStore


class CreateProfilePage:
    def __init__(self, app):
        self.app = app

    def build(self):
        platform_label = self.app.get_platform_label(self.app.current_platform_id)
        
        name_field = ft.TextField(
            label="Profile Name",
            hint_text="Enter a friendly name for this profile",
            bgcolor="#161b22",
            border_color="#21262d",
            focused_border_color="#238636"
        )
        
        token_field = ft.TextField(
            label="Access Token / API Key",
            hint_text="Enter your access token",
            password=True,
            can_reveal_password=True,
            bgcolor="#161b22",
            border_color="#21262d",
            focused_border_color="#238636"
        )
        
        owner_field = ft.TextField(
            label="Owner/Organization (optional)",
            hint_text="Enter owner or organization name",
            bgcolor="#161b22",
            border_color="#21262d",
            focused_border_color="#238636"
        )

        def save_profile(e):
            name = name_field.value.strip() if name_field.value else ""
            token = token_field.value.strip() if token_field.value else ""
            owner = owner_field.value.strip() if owner_field.value else ""
            
            if not name or not token:
                self.app.show_dialog("Missing Fields", "Name and token are required.")
                return
            
            profile = {
                "name": name,
                "token": token,
                "owner": owner or None,
                "created_at": datetime.utcnow().isoformat() + "Z",
            }
            
            ProfileStore.save_profile(self.app.current_platform_id, profile)
            self.app.show_dialog("Success", f"Profile '{name}' saved for {platform_label}.")
            self.app.open_platform(self.app.current_platform_id)

        return ft.Column([
            ft.Row([
                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda e: self.app.show_home(),
                    tooltip="Back to Home"
                ),
                ft.Text("Create Profile", size=28, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
            ]),
            ft.Text(f"Platform: {platform_label}", size=16, color="#8b949e"),
            ft.Container(height=24),
            ft.Container(
                content=ft.Column([
                    name_field,
                    token_field,
                    owner_field,
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
                width=400,
            )
        ])
