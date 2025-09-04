import flet as ft
from storage.profile_store import ProfileStore


class ProfilesPage:
    def __init__(self, app):
        self.app = app

    def build(self):
        profile_items = []
        
        for platform in self.app.platforms:
            profiles = ProfileStore.load_profiles(platform["id"])
            
            # Platform header
            profile_items.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(platform["icon"], color=platform["color"], size=24),
                            ft.Text(f"{platform['label']}", size=18, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Text(f"{len(profiles)}", color="#ffffff", size=12, weight=ft.FontWeight.BOLD),
                                bgcolor=platform["color"],
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=12,
                            ),
                        ]),
                        padding=16,
                        bgcolor="#161b22",
                        border_radius=8,
                    ),
                    elevation=1,
                )
            )
            
            # Profile items
            for profile in profiles:
                profile_items.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.PERSON, size=20, color="#8b949e"),
                                ft.Column([
                                    ft.Text(profile.get('name', 'Unnamed'), color="#f0f6fc", weight=ft.FontWeight.W_500),
                                    ft.Text(f"Created: {profile.get('created_at', 'Unknown')[:10]}", color="#8b949e", size=12),
                                ], spacing=2),
                                ft.Container(expand=True),
                                ft.IconButton(
                                    ft.Icons.EDIT,
                                    icon_color="#8b949e",
                                    tooltip="Edit Profile"
                                ),
                            ]),
                            padding=12,
                            bgcolor="#0d1117",
                            border_radius=6,
                        ),
                        elevation=0,
                    )
                )

        return ft.Column([
            ft.Row([
                ft.Text("Profiles", size=28, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Create Profile",
                    icon=ft.Icons.ADD,
                    on_click=lambda e: self.app.show_create_profile(),
                    bgcolor="#238636",
                    color="#ffffff"
                ),
            ]),
            ft.Container(height=16),
            ft.Column(profile_items, scroll=ft.ScrollMode.AUTO, expand=True, spacing=8),
        ])
