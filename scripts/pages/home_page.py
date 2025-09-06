import flet as ft
from storage.profile_store import ProfileStore
import json
import os


class HomePage:
    def __init__(self, app):
        self.app = app

    def build(self):
        # Get analytics data
        analytics = ProfileStore.get_analytics()
        deployment_analytics = self._get_deployment_analytics()
        
        # Analytics cards with deployment data
        analytics_cards = [
            self._create_stat_card("Total Projects", str(analytics["total_projects"]), ft.Icons.FOLDER, "#238636"),
            self._create_stat_card("Total Profiles", str(analytics["total_profiles"]), ft.Icons.PERSON, "#0969da"),
            self._create_stat_card("Total Deployments", str(deployment_analytics["total_deployments"]), ft.Icons.ROCKET_LAUNCH, "#8250df"),
            self._create_stat_card("Success Rate", f"{deployment_analytics['success_rate']:.1f}%", ft.Icons.CHECK_CIRCLE, "#238636"),
        ]
        
        # Platform cards with elevated buttons
        platform_cards = []
        
        for platform in self.app.platforms:
            platform_data = analytics["platforms"].get(platform["id"], {"profiles": 0, "projects": 0})
            deployment_data = deployment_analytics["by_platform"].get(platform["id"], {"count": 0, "success": 0})
            
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
                            weight=ft.FontWeight.W_500,
                            color="#f0f6fc"
                        ),
                        ft.Text(
                            f"{platform_data['profiles']} profiles • {deployment_data['count']} deployments",
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
            ft.Text("autoDeploy", size=32, weight=ft.FontWeight.W_500, color="#f0f6fc"),
            ft.Text("Multi-platform deployment management", size=16, color="#8b949e"),
            ft.Container(height=24),
            
            # Analytics section
            ft.Text("Analytics Overview", size=20, weight=ft.FontWeight.W_500, color="#f0f6fc"),
            ft.Container(height=12),
            ft.Row(analytics_cards, wrap=True, spacing=16),
            ft.Container(height=32),
            
            # Platforms section
            ft.Text("Deployment Platforms", size=20, weight=ft.FontWeight.W_500, color="#f0f6fc"),
            ft.Container(height=12),
            ft.Row(platform_cards, wrap=True, spacing=16),
        ], scroll=ft.ScrollMode.AUTO)

    def _create_stat_card(self, title: str, value: str, icon, color: str):
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=32, color=color),
                    ft.Column([
                        ft.Text(value, size=24, weight=ft.FontWeight.W_500, color="#f0f6fc"),
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

    def _get_deployment_analytics(self):
        """Get deployment analytics from deployments.json"""
        try:
            with open('data/deployments.json', 'r') as f:
                data = json.load(f)
            
            deployments = data.get('deployments', [])
            total = len(deployments)
            successful = len([d for d in deployments if d.get('status') == 'success'])
            
            by_platform = {}
            for deployment in deployments:
                platform = deployment.get('platform', 'unknown')
                if platform not in by_platform:
                    by_platform[platform] = {"count": 0, "success": 0}
                by_platform[platform]["count"] += 1
                if deployment.get('status') == 'success':
                    by_platform[platform]["success"] += 1
            
            return {
                "total_deployments": total,
                "successful_deployments": successful,
                "success_rate": (successful / total * 100) if total > 0 else 0,
                "by_platform": by_platform
            }
        except Exception:
            return {
                "total_deployments": 0,
                "successful_deployments": 0,
                "success_rate": 0,
                "by_platform": {}
            }
