import flet as ft
from ftp_plugin import generate_ftp_section
from speedtest_plugin import generate_speedtest_section
from isp_plugin import generate_ispinfo_section

def main(page: ft.Page):
    page.title = "BDIX Tool [JUNAID RAHMAN]"
    page.theme_mode = "dark"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "auto"

    ftp_section = generate_ftp_section(page)

    destinations = [
        ft.NavigationBarDestination(icon=ft.Icons.CLOUD_UPLOAD, label="FTP Servers"),
        ft.NavigationBarDestination(icon=ft.Icons.SPEED, label="Speed Test"),
        ft.NavigationBarDestination(icon=ft.Icons.INFO, label="ISP Information"),
    ]

    nav_bar = ft.NavigationBar(
        destinations=destinations,
        on_change=lambda e: update_content(e.control.selected_index),
    )

    speed_test_section = generate_speedtest_section(page)

    isp_info_section = generate_ispinfo_section(page)

    content = ftp_section

    def update_content(index):
        nonlocal content
        if index == 0:
            content = ftp_section
        elif index == 1:
            content = speed_test_section
        elif index == 2:
            content = isp_info_section
        page.clean()
        page.add(nav_bar, content)
        page.update()

    page.add(nav_bar, content)

ft.app(target=main)
