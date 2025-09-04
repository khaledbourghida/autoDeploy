import flet as ft


class PlatformDetailPage:
    def __init__(self, app):
        self.app = app

    def build(self):
        platform_label = self.app.get_platform_label(self.app.current_platform_id)
        actions = self.app.features_map.get(self.app.current_platform_id, [])
        
        action_cards = []
        for action in actions:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(action["icon"], size=40, color="#238636"),
                        ft.Text(
                            action["label"],
                            size=16,
                            weight=ft.FontWeight.BOLD,
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
                            on_click=lambda e, a=action: self.app.handle_action(a),
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
                ft.Text(platform_label, size=28, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
            ]),
            ft.Text("Choose an action to deploy", size=16, color="#8b949e"),
            ft.Container(height=24),
            ft.Row(action_cards, wrap=True, spacing=16),
        ], scroll=ft.ScrollMode.AUTO)
