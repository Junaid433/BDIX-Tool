import flet as ft
import requests
import threading

def generate_ftp_section(page: ft.Page):
    
    def import_from_file(e):
        def pick_files(e: ft.FilePickerResultEvent):
            if e.files:
                try:
                    with open(e.files[0].path, "r") as f:
                        urls = f.read().splitlines()
                        url_input.value = "\n".join(urls)
                        page.update()
                except Exception as ex:
                    print(f"Error reading file: {ex}")

        file_picker = ft.FilePicker(on_result=pick_files)
        page.overlay.append(file_picker)
        page.update()
        file_picker.pick_files(allowed_extensions=["txt"])

    def export_failed_urls(e):
        def save_file(e: ft.FilePickerResultEvent):
            if e.path:
                try:
                    with open(e.path, "w") as f:
                        failed_urls = [c.value for c in failed.controls]
                        f.write("Unsupported FTP URLs:\n" + "\n".join(failed_urls))
                except Exception as ex:
                    print(f"Error saving file: {ex}")

        file_picker = ft.FilePicker(on_result=save_file)
        page.overlay.append(file_picker)
        page.update()
        file_picker.save_file(file_name="", allowed_extensions=["txt"])

    def export_working_urls(e):
        def save_file(e: ft.FilePickerResultEvent):
            if e.path:
                try:
                    with open(e.path, "w") as f:
                        working_urls = [c.value for c in working.controls]
                        f.write("Working FTP URLs:\n" + "\n".join(working_urls))
                except Exception as ex:
                    print(f"Error saving file: {ex}")

        file_picker = ft.FilePicker(on_result=save_file)
        page.overlay.append(file_picker)
        page.update()
        file_picker.save_file(file_name="", allowed_extensions=["txt"])

    def load_ftps(e):
        url_input.value = open('bdix_ftp.txt', 'r').read()
        page.update()

    url_input = ft.TextField(
        label="Paste HTTP/HTTPS URLs (one per line)",
        multiline=True,
        min_lines=6,
        max_lines=8,
        expand=True,
        border_radius=8,
        border_color="blue",
        color=ft.colors.WHITE,
        suffix=ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        ft.icons.FILE_OPEN,
                        tooltip="Import BDIX FTP URLs From TXT File",
                        on_click=import_from_file,
                    ),
                    ft.IconButton(
                        ft.icons.BACKUP_TABLE,
                        tooltip="Load Popular BDIX FTPs",
                        on_click=load_ftps,
                    )
                ],
                spacing=0,
                tight=True,
            ),
            margin=0,
            padding=0
        )
    )

    timeout_input = ft.TextField(label="Timeout (ms)", value="5000", width=150, border_radius=8)
    threads_input = ft.TextField(label="Threads", value="1", width=100, border_radius=8)

    working = ft.ListView(expand=True, spacing=5)
    failed = ft.ListView(expand=True, spacing=5)

    working_title = ft.Text("✅ Supported FTP (0)", color=ft.colors.BLACK)
    failed_title = ft.Text("❌ Unsupported FTP (0)", color=ft.colors.BLACK)

    working_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    working_title,
                    ft.IconButton(ft.Icons.UPLOAD_FILE, tooltip="Save Supported FTP as TXT",
                                  on_click=export_working_urls, icon_color=ft.Colors.BLACK),
                ]),
                working
            ]),
            padding=10,
            bgcolor=ft.colors.GREEN_100,
            border_radius=10
        ),
        expand=True,
    )

    failed_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    failed_title,
                    ft.IconButton(ft.Icons.UPLOAD_FILE, tooltip="Save Unsupported FTP as TXT",
                                  on_click=export_failed_urls, icon_color=ft.Colors.BLACK),
                ]),
                failed
            ]),
            padding=10,
            bgcolor=ft.colors.RED_100,
            border_radius=10
        ),
        expand=True,
    )

    result_row = ft.Row(
        [
            ft.Container(working_card, expand=True, padding=5),
            ft.Container(failed_card, expand=True, padding=5),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    progress_bar = ft.ProgressBar(value=0, width=300, height=20)
    progress_text = ft.Text("0% (0/0)", size=12)

    def update_progress(processed, total):
        percent = int((processed / total) * 100) if total else 0
        progress_bar.value = percent / 100
        progress_text.value = f"{percent}% ({processed}/{total})"
        working_title.value = f"✅ Supported FTP ({len(working.controls)})"
        failed_title.value = f"❌ Unsupported FTP ({len(failed.controls)})"
        page.update()

    def check_urls(urls, timeout, num_threads):
        total_urls = len(urls)
        processed_urls = 0

        def check_url(url):
            nonlocal processed_urls
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    working.controls.append(ft.Text(url, color=ft.Colors.BLACK))
                else:
                    failed.controls.append(ft.Text(url, color=ft.Colors.BLACK))
            except:
                failed.controls.append(ft.Text(url, color=ft.Colors.BLACK))

            urls.remove(url)
            url_input.value = '\n'.join(urls)
            processed_urls += 1
            update_progress(processed_urls, total_urls)
            page.update()

        threads = []
        for url in urls:
            url = url.strip()
            if not url:
                continue
            thread = threading.Thread(target=check_url, args=(url,))
            threads.append(thread)

        def process_chunk(chunk):
            for thread in chunk:
                thread.start()
            for thread in chunk:
                thread.join()

        chunks = [threads[i:i + num_threads] for i in range(0, len(threads), num_threads)]
        for chunk in chunks:
            process_chunk(chunk)

        update_progress(total_urls, total_urls)

    def start_check(e):
        urls = url_input.value.strip().splitlines()
        for i in range(len(urls)):
            if 'http' not in urls[i]:
                urls[i] = 'http://' + urls[i]
        try:
            timeout = int(timeout_input.value) / 1000
            num_threads = int(threads_input.value)
        except:
            timeout = 3
            num_threads = 5

        working.controls.clear()
        failed.controls.clear()
        update_progress(0, len(urls))
        threading.Thread(target=check_urls, args=(urls, timeout, num_threads)).start()

    check_button = ft.ElevatedButton(
        "🚀 Start FTP Check",
        on_click=start_check,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=30, vertical=15),
            bgcolor=ft.colors.BLUE_ACCENT_700,
            color=ft.colors.WHITE,
        ),
    )

    ftp_section = ft.Column(
        [
            ft.Row([ft.Text("BDIX FTP Server Checker", size=20)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text("Check List of BDIX FTP Servers Supported By Your ISP")], alignment=ft.MainAxisAlignment.CENTER),
            url_input,
            ft.Row([timeout_input, threads_input], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([check_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([progress_bar, progress_text], alignment=ft.MainAxisAlignment.CENTER),
            result_row,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    return ftp_section
