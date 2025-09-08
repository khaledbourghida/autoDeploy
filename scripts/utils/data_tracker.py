import pandas as pd
import flet as ft
import datetime
import calendar

deployments = {
    "deployments": [
        {
            "platform": "github",
            "project_name": "my-app-github",
            "type": "repository",
            "status": "pending",
            "created_at": "2025-09-07T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "my-app-github",
            "type": "repository",
            "status": "pending",
            "created_at": "2025-09-07T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "my-app-github",
            "type": "repository",
            "status": "pending",
            "created_at": "2025-09-07T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "my-app-github",
            "type": "repository",
            "status": "pending",
            "created_at": "2025-09-06T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "my-app-github",
            "type": "repository",
            "status": "pending",
            "created_at": "2025-09-4T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "another-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-7T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "another-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-02T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "another-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-02T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "another-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-02T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "another-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-02T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "another-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-02T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "another-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-05T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "failed",
            "created_at": "2025-09-5T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "failed",
            "created_at": "2025-09-03T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "failed",
            "created_at": "2025-09-01T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "failed",
            "created_at": "2025-09-01T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "failed",
            "created_at": "2025-09-05T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "failed",
            "created_at": "2025-09-05T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "pending",
            "created_at": "2025-09-03T10:30:00Z"
        },{
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "pending",
            "created_at": "2025-09-03T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-01T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-01T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-03T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-03T10:30:00Z"
        },
        {
            "platform": "github",
            "project_name": "broken-github",
            "type": "repository",
            "status": "success",
            "created_at": "2025-09-03T10:30:00Z"
        },
        {
            "platform" : "github",
            "project_name" : "my-app-github",
            "type" : "repository",
            "status" : "pending",
            "created_at": "2025-09-4T10:30:00Z"
        },
        {
            "platform" : "github",
            "project_name" : "my-app-github",
            "type" : "repository",
            "status" : "failed",
            "created_at": "2025-09-01T10:30:00Z"
        },
        {
            "platform" : "netlify",
            "project_name" : "my-app-netlify",
            "type" : "site",
            "status" : "success",
            "created_at": "2025-09-4T10:30:00Z"
        },
        {
            "platform" : "render",
            "project_name" : "my-app-render",
            "type" : "web service",
            "status" : "failed",
            "created_at": "2025-03-15T10:30:00Z"
        }
    ]
}


def prepare_data(deployments: dict, platform: str):
        df = pd.DataFrame(deployments["deployments"])
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.date

        df = df[df["platform"] == platform]

        today = datetime.date.today()
        last_7_days = pd.date_range(today - pd.Timedelta(days=6), today, freq="D")

        grouped = df.groupby(["created_at", "status"]).size().reset_index(name="count")

        pivoted = grouped.pivot_table(
            index="created_at", columns="status", values="count", fill_value=0
        ).reindex(last_7_days.date, fill_value=0)

        for col in ["success", "pending", "failed"]:
            if col not in pivoted:
                pivoted[col] = 0

        pivoted = pivoted.reset_index(names="created_at")

        success_points = [
            ft.LineChartDataPoint((i + 1)*2, y)
            for i, y in enumerate(pivoted["success"])
        ]
        pending_points = [
            ft.LineChartDataPoint((i + 1)*2, y)
            for i, y in enumerate(pivoted["pending"])
        ]
        failed_points = [
            ft.LineChartDataPoint((i + 1)*2, y)
            for i, y in enumerate(pivoted["failed"])
        ]
        
        days = []
        for i in last_7_days:
            date = str(i).split(' ')[0].split('-')
            day = date[2]
            month = calendar.month_name[int(date[1])][:3]
            days.append(f'{month} {day}')

        return success_points, pending_points, failed_points, days