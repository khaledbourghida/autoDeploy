import flet as ft
from storage.profile_store import ProfileStore


class NetlifyFeaturesPage:
    def __init__(self, app):
        self.app = app

    def show_coming_soon_dialog(self):
        def close_dialog(e):
            self.coming_soon_dialog.open = False
            self.app.page.update()

        self.coming_soon_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Coming Soon", color="#f0f6fc"),
            content=ft.Text("Netlify integration is coming soon!", color="#8b949e"),
            actions=[
                ft.TextButton("OK", on_click=close_dialog)
            ],
            bgcolor="#161b22",
        )
        
        self.app.page.dialog = self.coming_soon_dialog
        self.coming_soon_dialog.open = True
        self.app.page.update()

    def build(self):
        netlify_actions = [
            {"id": "deploy_site", "label": "Deploy Site", "desc": "Deploy a site to Netlify", "icon": ft.Icons.CLOUD_UPLOAD},
            {"id": "list_sites", "label": "List Sites", "desc": "List all your Netlify sites", "icon": ft.Icons.LIST},
            {"id": "get_site", "label": "Get Site Info", "desc": "Get specific site details", "icon": ft.Icons.INFO},
            {"id": "update_site", "label": "Update Site", "desc": "Update site configuration", "icon": ft.Icons.EDIT},
            {"id": "delete_site", "label": "Delete Site", "desc": "Delete a site", "icon": ft.Icons.DELETE},
        ]
        
        action_cards = []
        for action in netlify_actions:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(action["icon"], size=40, color="#8b949e"),
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
                            "Coming Soon",
                            icon=ft.Icons.SCHEDULE,
                            on_click=lambda e: self.show_coming_soon_dialog(),
                            bgcolor="#8b949e",
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
                ft.Text("Netlify Features", size=28, weight=ft.FontWeight.W_500, color="#f0f6fc"),
            ]),
            ft.Text("Netlify integration coming soon", size=16, color="#8b949e"),
            ft.Container(height=24),
            ft.Row(action_cards, wrap=True, spacing=16),
        ], scroll=ft.ScrollMode.AUTO)
