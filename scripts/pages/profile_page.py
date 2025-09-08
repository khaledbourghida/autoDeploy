import flet as ft

class ProfilePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content = self.build_ui()
    
    def build_ui(self):
        return ft.Container(
            content=ft.Text(
                'Hello, I\'m khaled'
            ),
            width=200,
            height=200
        )
        
        