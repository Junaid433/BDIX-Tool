import flet as ft

def generate_speedtest_section(page: ft.Page):

    speedtest_section = ft.Column(
        [
            ft.Row([ft.Text("BDIX SpeedTest", size=20)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text("Check Your RealTime BDIX Speed")], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.WebView(
                url='https://fast.com/',
                enable_javascript = True,
                expand=True,
                height=1080,
                width=1920
            )
        ]
    )

    return speedtest_section
