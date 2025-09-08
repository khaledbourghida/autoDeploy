import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import asyncio
import flet as ft
from typing import List
import time
import datetime
from utils.data_tracker import deployments , prepare_data

colors = {
    'Gradient_1' : ["#0F4DD3" , '#3B82F6' , "#5C99FB" ],
    'Gradient_2' : ['#8B5CF6' , '#7C3AED'],
    'Gradient_3' : ["#E67F7F" , "#8B5CF6" , "#0F4DD3" , "#0F3C9D"],
    'Gradient_4' : ["#AC0F56" ,  "#CD1F6D" , '#EC4899'],
    'Warning_Attention' : ['#F59E0B' , '#D97706'],
    'Error_Alert' : ['#F87171' , '#DC2626'],
    'Neutral_CardBG' : '#161B22', 
    'Text_Colors' : {
        'primary' : '#E5E7EB',
        'secondary' : '#9CA3AF'
    }
}

class LineChart:
    def __init__(self):
        self.deployments = deployments
        self.platforms = ["github", "netlify", "render"]
        self.current_platform = "github"
        
        self.platform_label = ft.Text(self.current_platform.capitalize())

        # initial data
        self.success, self.pending, self.failed, self.last_7_day = prepare_data(
            self.deployments, self.current_platform
        )

        self.chart = self._build_chart()  # store chart instance
        self.platform_btn = self._build_platform_button()  # button for switching

    def _build_chart(self):
        data_series = [
            ft.LineChartData(
                data_points=self.success,
                stroke_width=3,
                color=ft.Colors.GREEN,
                curved=True,
                stroke_cap_round=True,
                below_line_gradient=ft.LinearGradient(
                    colors=[
                        ft.Colors.with_opacity(0.5, ft.Colors.GREEN),
                        ft.Colors.with_opacity(0.0, ft.Colors.GREEN),
                    ],
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                ),
            ),
            ft.LineChartData(
                data_points=self.pending,
                stroke_width=3,
                color=ft.Colors.ORANGE,
                curved=True,
                stroke_cap_round=True,
                below_line_gradient=ft.LinearGradient(
                    colors=[
                        ft.Colors.with_opacity(0.5, ft.Colors.ORANGE),
                        ft.Colors.with_opacity(0.0, ft.Colors.ORANGE),
                    ],
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                ),
            ),
            ft.LineChartData(
                data_points=self.failed,
                stroke_width=3,
                color=ft.Colors.RED,
                curved=True,
                stroke_cap_round=True,
                below_line_gradient=ft.LinearGradient(
                    colors=[
                        ft.Colors.with_opacity(0.5, ft.Colors.RED),
                        ft.Colors.with_opacity(0.0, ft.Colors.RED),
                    ],
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                ),
            ),
        ]

        return ft.LineChart(
            width=370,
            height=180,
            data_series=data_series,
            border=ft.border.only(
                left=ft.BorderSide(2, ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE)),
                bottom=ft.BorderSide(2, ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE)),
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=2, color=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE), width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=2, color=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE), width=1
            ),
            left_axis=ft.ChartAxis(
                labels=[ft.ChartAxisLabel(value=i, label=ft.Text(str(i), size=10)) for i in range(0, 9, 2)],
                labels_size=20,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=(i + 1) * 2,
                        label=ft.Container(
                            ft.Text(
                                day,
                                size=10,
                                color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    )
                    for i, day in enumerate(self.last_7_day)
                ],
                labels_size=22,
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
            min_y=0,
            max_y=8,
            min_x=0,
            max_x=15,
            expand=True,
        )

    def _build_platform_button(self):
        return ft.PopupMenuButton(
            icon=ft.Icons.ARROW_DROP_DOWN,
            items=[
                ft.PopupMenuItem(text=p.capitalize(), on_click=lambda e, p=p: self._switch_platform(p))
                for p in self.platforms
            ],
        )

    def _switch_platform(self, platform: str):
        # update platform
        self.current_platform = platform
        self.platform_label.value = platform.capitalize()  # ✅ update the label
        self.platform_label.update()
        self.success, self.pending, self.failed, self.last_7_day = prepare_data(
            self.deployments, self.current_platform
        )

        # update chart data
        self.chart.data_series = [
            ft.LineChartData(self.success, stroke_width=3, color=ft.Colors.GREEN, curved=True, below_line_gradient=ft.LinearGradient(
                    colors=[
                        ft.Colors.with_opacity(0.5, ft.Colors.GREEN),
                        ft.Colors.with_opacity(0.0, ft.Colors.GREEN),
                    ],
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                ),),
            ft.LineChartData(self.pending, stroke_width=3, color=ft.Colors.ORANGE, curved=True , below_line_gradient=ft.LinearGradient(
                    colors=[
                        ft.Colors.with_opacity(0.5, ft.Colors.ORANGE),
                        ft.Colors.with_opacity(0.0, ft.Colors.ORANGE),
                    ],
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                ),),
            ft.LineChartData(self.failed, stroke_width=3, color=ft.Colors.RED, curved=True , below_line_gradient=ft.LinearGradient(
                    colors=[
                        ft.Colors.with_opacity(0.5, ft.Colors.RED),
                        ft.Colors.with_opacity(0.0, ft.Colors.RED),
                    ],
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                ),),
        ]
        self.chart.bottom_axis = ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=(i + 1) * 2,
                    label=ft.Container(ft.Text(day, size=10, color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE)))
                )
                for i, day in enumerate(self.last_7_day)
            ],
            labels_size=22,
        )
        self.chart.update()

    def build_line_chart(self):
        return ft.Column(
            [
                ft.Row([self.platform_label, self.platform_btn]),
                self.chart,
            ]
        )

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.chart = LineChart().build_line_chart()
        self.content = self.build_ui()
        
        
    def circle_grad(self , color : List):
        gradient_circle = ft.Container(
            width=300,
            height=300,
            border_radius=150,
            gradient=ft.RadialGradient(
                center=ft.Alignment(0, 0),
                radius=1.0,
                colors=[
                    color[0],
                    ft.Colors.with_opacity(0.0, color[1]),
                ],
                stops=[0.0, 1.0],
            ),
        )

        return ft.Container(
            content=gradient_circle,
            alignment=ft.alignment.bottom_left,
            left=-150,
            bottom=-150,
        )
    
    def desc_card(self , desc_text : List):
        return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            desc_text[0],
                            size=18,
                            color=colors['Text_Colors']['primary'],
                        ),
                        ft.Text(
                            desc_text[1],
                            weight=ft.FontWeight.W_500,
                            size=45,
                            color=colors['Text_Colors']['primary']
                        ),
                    ]
                ),
                alignment=ft.alignment.center,
                left=30,
                bottom=27
        )
        
    
    def build_projects_list(self):
        deployments_list = [
            {
                "platform" : "github",
                "project_name" : "my-app-github",
                "type" : "repository",
                "status" : "pending"
            },
            {
                "platform" : "netlify",
                "project_name" : "my-app-netlify",
                "type" : "site",
                "status" : "success"
            },
            {
                "platform" : "render",
                "project_name" : "my-app-render",
                "type" : "web service",
                "status" : "failed"
            }
        ]
        colors_state = {
            "success": ft.Colors.GREEN,
            "pending": ft.Colors.AMBER,
            "failed": ft.Colors.RED,
        }
        
        deployment_card = []
        for deployment in deployments_list:
            card = ft.Container(
                expand=True,
                content=ft.Row(
                    
                    controls=[
                        ft.Image(
                            src=f'assets/photos/{deployment['platform']}.png',
                            width=30,
                            height=30,
                        ),
                        ft.Container(width=10),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    f'{deployment['project_name']} ({deployment['type']})',
                                    size=15,
                                    color=colors['Text_Colors']['primary'],
                                    no_wrap=True,
                                ),
                                ft.Text(
                                    f'{deployment['status']}',
                                    size=12,
                                    color=colors_state[f'{deployment["status"]}']
                                )
                            ]
                        )
                    ]
                ),
            )
            deployment_card.append(card)
            deployment_card.append(ft.Divider(height=1, color="#21262d"))
            
            
        return deployment_card

    def build_countdown(self , page: ft.Page, reset_timestamp: int):

        countdown_text = ft.Text(
            value="Loading...",
            size=20,
            color="white",
            weight=ft.FontWeight.BOLD,
        )

        async def _updater():
            # Wait until the text is attached to the page
            while getattr(countdown_text, "page", None) is None:
                await asyncio.sleep(0.05)

            while True:
                now = int(time.time())
                remaining = reset_timestamp - now
                if remaining <= 0:
                    countdown_text.value = "Reset!"
                else:
                    td = datetime.timedelta(seconds=remaining)
                    # Format as HH:MM:SS if less than 1 day
                    countdown_text.value = str(td) if td.days else str(datetime.timedelta(seconds=remaining))
                try:
                    countdown_text.update()
                except AssertionError:
                    pass  # safe-guard in case page is not ready
                await asyncio.sleep(1)

        page.run_task(_updater)

        return countdown_text
        
        
    # Home content area
    def build_ui(self):
        return ft.Container(
            expand=True,
            bgcolor=None,
            content=ft.Column(
                controls=[
                    ft.Container(
                        expand=1,
                        bgcolor=None,
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            'Dashboard',
                                            color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD,
                                            size=30
                                        ),
                                        ft.Text(
                                            'See all your data here , profiles , projects , rate limits',
                                            color=ft.Colors.with_opacity(0.3 , "#9e9e9e"),
                                            size=15,
                                        )
                                    ]
                                ),
                                ft.Container(
                                    width=600,
                                ),
                                ft.ElevatedButton(
                                    'Add Project',
                                    icon=ft.Icons.ADD,
                                    bgcolor='#162441',
                                    color = ft.Colors.WHITE                                  
                                )
                            ]
                        ),
                    ),
                    ft.Container(
                       expand=2,
                       bgcolor=None,
                       content=ft.Row(
                           controls=[
                               ft.Container(
                                   padding=20,
                                   expand=True,
                                   bgcolor='#161b22',
                                   border_radius=20,
                                   content=ft.Column(
                                       controls=[
                                           ft.Text(
                                               'Total Deployments',
                                               size=18,
                                               color=colors['Neutral_CardBG'],
                                           ),
                                           ft.Text(
                                               '24',
                                               weight=ft.FontWeight.W_500,
                                               size=45,
                                               color=colors['Neutral_CardBG']
                                           ),
                                           ft.Row(
                                               controls=[
                                                   ft.Icon(
                                                       ft.Icons.ALL_INBOX,
                                                       size=18,
                                                       color=colors['Text_Colors']['secondary']
                                                   ),
                                                   ft.Text(
                                                       'All deployments from all platforms',
                                                       size=12,
                                                       color=ft.Colors.with_opacity(0.5 , ft.Colors.WHITE),
                                                   )
                                               ]
                                           )
                                       ]
                                   ),
                                    ink=True,
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left,
                                        end=ft.alignment.bottom_right,
                                        colors=colors['Gradient_3'],
                                    ),
                                ),
                               ft.Container(
                                   expand=True,
                                   bgcolor=colors['Neutral_CardBG'],
                                   border_radius=20,
                                   content=ft.Stack(
                                       controls=[
                                            # self.circle_grad([ft.Colors.GREEN , "green"]),
                                            self.desc_card(["Success Deployments" , "10"])
                                       ]
                                   )
                               ),
                               ft.Container(
                                   expand=True,
                                   bgcolor=colors['Neutral_CardBG'],
                                   border_radius=20,
                                   content=ft.Stack(
                                       controls=[
                                            # self.circle_grad([ft.Colors.RED , "red"]),
                                            self.desc_card(["Failed Deployments" , "12"])
                                       ]
                                   )
                               ),
                               ft.Container(
                                   expand=True,
                                   bgcolor=colors['Neutral_CardBG'],
                                   border_radius=20,
                                   content=ft.Stack(
                                       controls=[
                                            # self.circle_grad([ft.Colors.ORANGE , "orange"]),
                                            self.desc_card(["Pending Deployments" , "2"])
                                       ]
                                   )
                               ),
                           ]
                       )
                    ),
                    ft.Container(
                       expand=5,
                       content=ft.Row(
                           controls=[
                               #================
                               ft.Container(
                                   expand=3,
                                   content=ft.Column(
                                       controls=[
                                           ft.Container(
                                               expand=2,
                                               content=ft.Row(
                                                   controls=[
                                                       ft.Container(
                                                           expand=2,
                                                           border_radius=20,
                                                           padding=10,
                                                           border=ft.Border(ft.BorderSide(1 , ft.Colors.BLUE_GREY) , ft.BorderSide(1 , ft.Colors.BLUE_GREY) , ft.BorderSide(1 , ft.Colors.BLUE_GREY) , ft.BorderSide(1 , ft.Colors.BLUE_GREY) ,),
                                                           content=ft.Row([
                                                                ft.Container(
                                                                    expand=2,
                                                                    gradient=ft.LinearGradient(
                                                                        colors=["#072E84" , "#051E56" , "#02102C"],
                                                                        begin=ft.alignment.center_right,
                                                                        end=ft.alignment.center_left
                                                                    ),
                                                                    border_radius=20,
                                                                    alignment=ft.alignment.center,
                                                                    content=ft.Stack([
                                                                        ft.Column(
                                                                            left=35,
                                                                            controls=[
                                                                            ft.Text(
                                                                                'GitHub',
                                                                                size=20,
                                                                                weight=ft.FontWeight.BOLD,
                                                                                color = colors['Text_Colors']['primary']
                                                                            ),
                                                                            ft.Image(
                                                                                src = 'assets/photos/github.png',
                                                                                width=70,
                                                                                height=70
                                                                            )
                                                                        ]),
                                                                        ft.Container(
                                                                            expand=True,
                                                                            bgcolor=ft.Colors.with_opacity(0.3 , ft.Colors.BLACK)
                                                                        ),
                                                                        
                                                                    ]),
                                                                ),
                                                                ft.Container(
                                                                    expand=2,
                                                                    gradient=ft.LinearGradient(
                                                                        colors=["#07840F" , "#055611" , "#022C07"],
                                                                        begin=ft.alignment.center_right,
                                                                        end=ft.alignment.center_left
                                                                    ),
                                                                    border_radius=20,
                                                                    alignment=ft.alignment.center,
                                                                    content=ft.Stack([
                                                                        ft.Column(
                                                                            left=35,
                                                                            controls=[
                                                                            ft.Text(
                                                                                'Netlify',
                                                                                size=20,
                                                                                weight=ft.FontWeight.BOLD,
                                                                                color = colors['Text_Colors']['primary']
                                                                            ),
                                                                            ft.Image(
                                                                                src = 'assets/photos/netlify.png',
                                                                                width=70,
                                                                                height=70
                                                                            )
                                                                        ]),
                                                                        ft.Container(
                                                                            expand=True,
                                                                            bgcolor=ft.Colors.with_opacity(0.3 , ft.Colors.BLACK)
                                                                        ),
                                                                        
                                                                    ]),
                                                                ),
                                                                ft.Container(
                                                                    expand=2,
                                                                    gradient=ft.LinearGradient(
                                                                        colors=["#84077C" , "#56054E" , "#2C0224"],
                                                                        begin=ft.alignment.center_right,
                                                                        end=ft.alignment.center_left
                                                                    ),
                                                                    border_radius=20,
                                                                    alignment=ft.alignment.center,
                                                                    content=ft.Stack([
                                                                        ft.Column(
                                                                            left=35,
                                                                            controls=[
                                                                            ft.Text(
                                                                                'Render',
                                                                                size=20,
                                                                                weight=ft.FontWeight.BOLD,
                                                                                color = colors['Text_Colors']['primary']
                                                                            ),
                                                                            ft.Image(
                                                                                src = 'assets/photos/render.png',
                                                                                width=70,
                                                                                height=70
                                                                            )
                                                                        ]),
                                                                        ft.Container(
                                                                            expand=True,
                                                                            bgcolor=ft.Colors.with_opacity(0.3 , ft.Colors.BLACK)
                                                                        ),
                                                                        
                                                                    ]),
                                                                ),
                                                                ft.Container(
                                                                    expand=1,
                                                                    alignment=ft.alignment.center,
                                                                    content=ft.Container(
                                                                        alignment=ft.alignment.center,
                                                                        border_radius=50,
                                                                        height=60,
                                                                        width=60,
                                                                        border=ft.Border(ft.BorderSide(1 , ft.Colors.BLUE_GREY) , ft.BorderSide(1 , ft.Colors.BLUE_GREY) , ft.BorderSide(1 , ft.Colors.BLUE_GREY) , ft.BorderSide(1 , ft.Colors.BLUE_GREY) ,),
                                                                        content=ft.IconButton(
                                                                            icon=ft.Icons.ARROW_FORWARD_IOS,
                                                                            icon_color=colors['Text_Colors']['primary'],
                                                                            icon_size=20
                                                                        )
                                                                    )
                                                                ),
                                                           ]),
                                                       ),
                                                       ft.Container(
                                                           expand=1,
                                                           bgcolor='#161b22',
                                                           border_radius=20,
                                                           content=ft.Stack([
                                                               ft.Image(
                                                                   src='assets/photos/cardBg.jpg',
                                                                   fit=ft.ImageFit.COVER,
                                                                   height=300,
                                                                ),
                                                               ft.Container(
                                                                   expand=True,
                                                                   bgcolor=ft.Colors.with_opacity(0.5 , ft.Colors.BLACK),
                                                               ),
                                                               ft.Container(
                                                                   content=ft.Text(
                                                                       'Remaining Req :',
                                                                       size=16,
                                                                       weight=ft.FontWeight.W_500
                                                                   ),
                                                                   bottom=120,
                                                                   left=30,
                                                               ),
                                                               ft.Container(
                                                                   alignment=ft.alignment.center,
                                                                   content=ft.Text(
                                                                       '5000',
                                                                       size=30,
                                                                       weight=ft.FontWeight.BOLD
                                                                   )
                                                               ),
                                                               ft.Container(
                                                                   alignment=ft.alignment.bottom_center,
                                                                    width=170,
                                                                    height=32,
                                                                    border_radius=30,
                                                                    ink=True,
                                                                    gradient=ft.LinearGradient(
                                                                        begin=ft.alignment.top_left,
                                                                        end=ft.alignment.bottom_right,
                                                                        colors=colors['Gradient_3'],
                                                                    ),
                                                                    left=50,
                                                                    bottom=10,
                                                               ),
                                                               ft.Row(
                                                                    alignment=ft.alignment.bottom_center,
                                                                    controls=[
                                                                        ft.Icon(ft.Icons.ADD , size=15 , color=colors['Text_Colors']['primary'] , weight=ft.FontWeight.W_500),
                                                                        ft.Text('Create Deployment' , size=13 , color=colors['Text_Colors']['primary'] ,  weight=ft.FontWeight.W_500)
                                                                    ],
                                                                    left=60,
                                                                    bottom=17,
                                                                ),
                                                           ])
                                                       )
                                                   ]
                                               )
                                           ),
                                           ft.Container(
                                               expand=3,
                                               content=ft.Row(
                                                   controls=[
                                                       ft.Container(
                                                            expand=True,
                                                            bgcolor='#161b22',
                                                            border_radius=20,
                                                            content=self.chart,
                                                            alignment=ft.alignment.center,
                                                            padding=10,
                                                        ),
                                                       ft.Container(
                                                           expand=True,
                                                           bgcolor='#161b22',
                                                           border_radius=20,
                                                       ),
                                                   ]
                                               )
                                           ),
                                       ]
                                   )
                               ),
                               #=================
                               ft.Container(
                                   expand=1,
                                   content=ft.Column(
                                       controls=[
                                           ft.Container(
                                               padding=20,
                                               expand=2,
                                               bgcolor='#161b22',
                                               border_radius=20,
                                               content=ft.Column(
                                                   controls=[
                                                       ft.Row(
                                                           controls=[
                                                               ft.Text(
                                                                   'Deployments',
                                                                   color=colors['Text_Colors']['primary'],
                                                                   size=20,
                                                               ),
                                                               ft.Container(width=35),
                                                               ft.ElevatedButton(
                                                                   'New',
                                                                   icon=ft.Icons.ADD,
                                                                   color=colors['Text_Colors']['primary'],
                                                                   bgcolor=colors['Neutral_CardBG'],
                                                                   style=ft.ButtonStyle(
                                                                       side=ft.BorderSide(2,colors['Text_Colors']['primary'])
                                                                   )
                                                               )
                                                           ]
                                                        ),
                                                       ft.Container(height=10),
                                                       ft.ListView(controls=self.build_projects_list(), expand=True, spacing=5),

                                                   ]
                                               )
                                           ),
                                           ft.Container(
                                               expand=1,
                                               bgcolor='#161b22',
                                               border_radius=20,
                                               content=ft.Stack(
                                                   controls=[
                                                        ft.Image(
                                                            src='assets/photos/cardBg.jpg',
                                                            fit=ft.ImageFit.COVER,
                                                            height=200,
                                                            width=300
                                                        ),
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=ft.Colors.with_opacity(0.5 , ft.Colors.BLACK)
                                                        ),
                                                        ft.Container(
                                                            content=ft.Text('rate limit reset after :' , color=colors['Text_Colors']['primary'] , size=16 , weight=ft.FontWeight.W_600),
                                                            alignment=ft.alignment.top_left,
                                                            left=20,
                                                            bottom=95,
                                                            
                                                        ),
                                                        ft.Container(
                                                            content=self.build_countdown(self.page, 1757199654),
                                                            alignment=ft.alignment.center
                                                        )
                                                   ]
                                               )
                                           )
                                       ]
                                   )
                               )
                           ]
                       )
                    )
                ]
            )
        )