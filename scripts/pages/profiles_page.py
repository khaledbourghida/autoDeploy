import flet as ft
from storage.profile_store import ProfileStore


class ProfilesPage:
    def __init__(self, app):
        self.app = app

    def show_platform_selection_dialog(self, e):
        def close_dialog(e):
            self.platform_dialog.open = False
            self.app.page.update()

        def select_platform(e, platform_id):
            close_dialog(e)
            self.app.current_platform_id = platform_id
            self.app.show_create_profile()

        platform_buttons = []
        for platform in self.app.platforms:
            platform_buttons.append(
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(platform["icon"], color=platform["color"], size=20),
                        ft.Text(platform["label"], color="#ffffff")
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=lambda e, pid=platform["id"]: select_platform(e, pid),
                    bgcolor=platform["color"],
                    color="#ffffff",
                    width=200
                )
            )

        self.platform_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Select Platform", color="#f0f6fc"),
            content=ft.Column([
                ft.Text("Choose a platform to create a profile for:", color="#8b949e"),
                ft.Container(height=16),
                ft.Column(platform_buttons, spacing=12)
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog)
            ],
            bgcolor="#161b22",
        )
        
        self.app.page.dialog = self.platform_dialog
        self.platform_dialog.open = True
        self.app.page.update()

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
                                    ft.Text(profile.get('username', 'Unnamed'), color="#f0f6fc", weight=ft.FontWeight.W_500),
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
                    on_click=lambda e: self.show_platform_selection_dialog(e),
                    bgcolor="#238636",
                    color="#ffffff"
                ),
            ]),
            ft.Container(height=16),
            ft.Column(profile_items, scroll=ft.ScrollMode.AUTO, expand=True, spacing=8),
        ])
