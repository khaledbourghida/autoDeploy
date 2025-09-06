import flet as ft
from storage.profile_store import ProfileStore
import json
import os


class GitHubFeaturesPage:
    def __init__(self, app):
        self.app = app
        self.profiles = ProfileStore.load_profiles('github')

    def show_profiles_dialog(self):
        """Build and show the profiles dialog"""
        content = ft.Column(scroll=ft.ScrollMode.AUTO, tight=True)

        if not self.profiles:
            content.controls.append(ft.Text("No profiles found."))
        else:
            content.controls.append(ft.Text("Select one:"))
            for profile in self.profiles:
                btn = ft.TextButton(
                    text=profile.get("name", "Unnamed Profile"),
                    on_click=lambda e, p=profile: self._handle_profile_click(p),
                )
                content.controls.append(btn)

        # Create dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Choose a GitHub Profile"),
            content=content,
            actions=[
                ft.TextButton("Close", on_click=lambda e: self._close_dialog())
            ]
        )

        # Attach to page BEFORE opening
        self.app.page.dialog = self.dialog
        self.dialog.open = True
        self.app.page.update()

    def _close_dialog(self):
        self.dialog.open = False
        self.app.page.update()

    def _handle_profile_click(self, profile):
        self._close_dialog()
        print(f"Selected profile: {profile}")  # Replace with your real logic

    def build(self):
        github_actions = [
            {"id": "repository", "label": "Repository Management", "desc": "Manage your repository actions", "icon": ft.Icons.CREATE_NEW_FOLDER},
            {"id": "github_pages", "label": "Github Pages", "desc": "Manage your github pages", "icon": ft.Icons.WEB},
            {"id": "user", "label": "User Management", "desc": "Manage your personal informations", "icon": ft.Icons.PERSON},
            {"id": "collaborators", "label": "Collaborators", "desc": "Manage your collaborators", "icon": ft.Icons.PERSON_3},
            {"id": "release", "label": "Releases", "desc": "Manage your releases", "icon": ft.Icons.ROCKET_LAUNCH},
            {"id": "actions", "label": "Actions", "desc": "Manage your actions", "icon": ft.Icons.WORK},
        ]
        
        action_cards = []
        for action in github_actions:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(action["icon"], size=40, color="#238636"),
                        ft.Text(
                            action["label"],
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color="#f0f6fc"
                        ),
                        ft.Text(
                            action["desc"],
                            size=12,
                            color="#8b949e",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.ElevatedButton(
                            "Execute",
                            icon=ft.Icons.PLAY_ARROW,
                            on_click=lambda e: self.show_profiles_dialog(),
                            bgcolor="#238636",
                            color="#ffffff",
                            width=120
                        ),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8),
                    padding=20,
                    width=240,
                    height=180,
                    bgcolor="#161b22",
                    border_radius=12,
                ),
                elevation=2,
            )
            action_cards.append(card)

        return ft.Column([
            ft.Row([
                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda e: self.app.show_home(),
                    tooltip="Back to Home"
                ),
                ft.Text("GitHub Features", size=28, weight=ft.FontWeight.W_500, color="#f0f6fc"),
            ]),
            ft.Text("Choose a GitHub action to execute", size=16, color="#8b949e"),
            ft.Container(height=24),
            ft.Row(action_cards, wrap=True, spacing=16 ),
        ], scroll=ft.ScrollMode.AUTO)
