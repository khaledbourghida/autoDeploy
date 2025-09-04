import flet as ft
from data.profile_store import ProfileStore


class HomePage:
    def __init__(self, app):
        self.app = app

    def build(self):
        # Get analytics data
        analytics = ProfileStore.get_analytics()
        
        # Analytics cards
        analytics_cards = [
            self._create_stat_card("Total Projects", str(analytics["total_projects"]), ft.Icons.FOLDER, "#238636"),
            self._create_stat_card("Total Profiles", str(analytics["total_profiles"]), ft.Icons.PERSON, "#0969da"),
            self._create_stat_card("Active Platforms", str(len([p for p in analytics["platforms"].values() if p["profiles"] > 0])), ft.Icons.CLOUD, "#8250df"),
        ]
        
        # Platform cards with elevated buttons
        platform_cards = []
        
        for platform in self.app.platforms:
            platform_data = analytics["platforms"].get(platform["id"], {"profiles": 0, "projects": 0})
            
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(
                            platform["icon"],
                            size=48,
                            color=platform["color"]
                        ),
                        ft.Text(
                            platform["label"],
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#f0f6fc"
                        ),
                        ft.Text(
                            f"{platform_data['profiles']} profiles • {platform_data['projects']} projects",
                            size=12,
                            color="#8b949e"
                        ),
                        ft.Container(height=8),
                        ft.ElevatedButton(
                            "Open Platform",
                            icon=ft.Icons.ARROW_FORWARD,
                            on_click=lambda e, pid=platform["id"]: self.app.open_platform(pid),
                            bgcolor=platform["color"],
                            color="#ffffff",
                            width=160
                        ),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8),
                    padding=24,
                    width=220,
                    height=200,
                    bgcolor="#161b22",
                    border_radius=12,
                ),
                elevation=3,
            )
            platform_cards.append(card)

        return ft.Column([
            ft.Text("autoDeploy", size=32, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
            ft.Text("Multi-platform deployment management", size=16, color="#8b949e"),
            ft.Container(height=24),
            
            # Analytics section
            ft.Text("Analytics Overview", size=20, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
            ft.Container(height=12),
            ft.Row(analytics_cards, spacing=16),
            ft.Container(height=32),
            
            # Platforms section
            ft.Text("Deployment Platforms", size=20, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
            ft.Container(height=12),
            ft.Row(platform_cards, wrap=True, spacing=16),
        ], scroll=ft.ScrollMode.AUTO)

    def _create_stat_card(self, title: str, value: str, icon, color: str):
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=32, color=color),
                    ft.Column([
                        ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color="#f0f6fc"),
                        ft.Text(title, size=12, color="#8b949e"),
                    ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.START, spacing=16),
                padding=20,
                width=200,
                height=80,
                bgcolor="#161b22",
                border_radius=12,
            ),
            elevation=2,
        )
