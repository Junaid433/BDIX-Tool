import flet as ft
import requests
from bs4 import BeautifulSoup

def generate_ispinfo_section(page: ft.Page):
    # Get the user's public IP
    ip = requests.get('https://ifconfig.me/').text.strip()

    # Get the ISP information using Scamalytics
    ip_info = requests.get(f'https://scamalytics.com/ip/{ip}').text
    soup = BeautifulSoup(ip_info, 'html.parser')

    # Extract relevant ISP information from the HTML
    data = {}
    rows = soup.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if cols:
            title = row.find_previous('th').get_text(strip=True)  # Get the corresponding title
            value = cols[0].get_text(strip=True)  # Get the data value
            data[title] = value

    # Create the Flet UI with cool design
    ispinfo_section = ft.Column(
        [
            ft.Row([ft.Text("ISP Information", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text(f"ISP: {data.get('ASN', 'N/A')}", size=18)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text(f"IP Address: {ip}", size=18)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            
            # Adding a styled box for each section
            ft.Row([ft.Text("Operator Details", size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Hostname: {data.get('Hostname', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"ASN: {data.get('ASN', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"ISP Name: {data.get('ISP Name', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Organization Name: {data.get('Organization Name', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),

            ft.Row([ft.Text("Location Details", size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Country: {data.get('Country Name', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Region: {data.get('State / Province', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"City: {data.get('City', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Latitude: {data.get('Latitude', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Longitude: {data.get('Longitude', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),

            ft.Row([ft.Text("Proxy & Datacenter", size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Datacenter: {data.get('Datacenter', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Anonymizing VPN: {data.get('Anonymizing VPN', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Tor Exit Node: {data.get('Tor Exit Node', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Server: {data.get('Server', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Public Proxy: {data.get('Public Proxy', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),

            ft.Row([ft.Text("Blacklist Status", size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Firehol: {data.get('Firehol', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"IP2ProxyLite: {data.get('IP2ProxyLite', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"IPsum: {data.get('IPsum', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"Spamhaus: {data.get('Spamhaus', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Row([ft.Text(f"X4Bnet Spambot: {data.get('X4Bnet Spambot', 'N/A')}", size=16)], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12  # Adding space between elements for better layout
    )

    return ispinfo_section
