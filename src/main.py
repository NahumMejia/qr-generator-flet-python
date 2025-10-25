import flet as ft
import qrcode
from io import BytesIO
import base64
import os

def main(page: ft.Page):
    page.title = "QR Code Generator"
    page.scroll = None
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 12

    # Available colors for QR codes (name and hex value)
    colors = {
        "black": "#000000", "white": "#FFFFFF", "red": "#FF0000", "green": "#008000",
        "blue": "#0000FF", "yellow": "#FFFF00", "orange": "#FFA500", "purple": "#800080",
        "pink": "#FFC0CB", "brown": "#A52A2A", "gray": "#808080", "cyan": "#00FFFF",
        "magenta": "#FF00FF", "lime": "#00FF00", "navy": "#000080", "teal": "#008080",
        "maroon": "#800000", "olive": "#808000", "silver": "#C0C0C0", "gold": "#FFD700"
    }

    current_qr_image = None

    # Embed icon as base64
    icon_b64 = None
    for p in ("src/assets/icon.png", "assets/icon.png", "icon.png"):
        if os.path.exists(p):
            with open(p, "rb") as f:
                icon_b64 = base64.b64encode(f.read()).decode()
            break

    app_logo = ft.Image(
        src_base64=icon_b64 if icon_b64 else None,
        width=140,
        height=140,
        fit=ft.ImageFit.CONTAIN
    )

    # Title 
    title_text = ft.Text(value="Wisecode QR Code Generator", size=30, weight=ft.FontWeight.W_100)

    # Header 
    header = ft.Column(
        [app_logo, title_text],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=2,   # casi pegado
    )

    # URL input
    url_input = ft.TextField(
        label="URL",
        width=360,
        hint_text="https://example.com",
        dense=True
    )

    # Dropdowns
    background_color_dropdown = ft.Dropdown(
        label="Background", width=140, value="white", dense=True,
        options=[ft.dropdown.Option(key=c, text=c.capitalize()) for c in colors.keys()]
    )
    code_color_dropdown = ft.Dropdown(
        label="Code color", width=140, value="black", dense=True,
        options=[ft.dropdown.Option(key=c, text=c.capitalize()) for c in colors.keys()]
    )
    border_dropdown = ft.Dropdown(
        label="Border", width=110, value="4", dense=True,
        options=[ft.dropdown.Option(key=str(n), text=str(n)) for n in (1,2,3,4,5,6,8)]
    )

    controls_row = ft.Row(
        controls=[background_color_dropdown, code_color_dropdown, border_dropdown],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8
    )

    # Preview
    preview_title = ft.Text("QR Preview", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    preview_content = ft.Text("Generate to see the QR code", size=13, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY_600)
    preview_box = ft.Container(
        content=preview_content, width=150, height=150,
        border=ft.border.all(2, ft.Colors.GREY_400),
        alignment=ft.alignment.center, bgcolor=ft.Colors.GREY_100
    )

    def generate_qr(e):
        nonlocal current_qr_image
        url = url_input.value
        if not url:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter a URL"))
            page.snack_bar.open = True; page.update(); return
        if code_color_dropdown.value == background_color_dropdown.value:
            page.snack_bar = ft.SnackBar(content=ft.Text("Code color and background color must be different!"))
            page.snack_bar.open = True; page.update(); return
        try:
            fill_color = colors[code_color_dropdown.value]
            back_color = colors[background_color_dropdown.value]
            border_size = int(border_dropdown.value)

            qr = qrcode.QRCode(
                version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10, border=border_size
            )
            qr.add_data(url); qr.make(fit=True)
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            current_qr_image = img

            buffer = BytesIO(); img.save(buffer, format='PNG'); buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()

            preview_box.content = ft.Image(
                src_base64=img_base64, width=200, height=200, fit=ft.ImageFit.CONTAIN
            )
            page.snack_bar = ft.SnackBar(content=ft.Text(f"QR generated: {code_color_dropdown.value} on {background_color_dropdown.value}"))
            page.snack_bar.open = True; page.update()
        except Exception as ex:
            import traceback; traceback.print_exc()
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"))
            page.snack_bar.open = True; page.update()

    def download_qr(e):
        if current_qr_image is None:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please generate a QR code first"))
            page.snack_bar.open = True; page.update(); return
        try:
            filename = "qrcode.png"
            current_qr_image.save(filename)
            page.snack_bar = ft.SnackBar(content=ft.Text(f"QR Code saved as {filename}"), duration=3000)
            page.snack_bar.open = True; page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error saving: {str(ex)}"))
            page.snack_bar.open = True; page.update()

    # Buttons
    generate_button = ft.ElevatedButton(text="GENERATE", icon=ft.Icons.QR_CODE, width=160, on_click=generate_qr, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    download_button = ft.ElevatedButton(text="DOWNLOAD", icon=ft.Icons.DOWNLOAD, width=160, on_click=download_qr, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)

    buttons_row = ft.Row(
        controls=[generate_button, download_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8
    )

    # Layout
    page.add(
        header,
        ft.Container(height=6),
        url_input,
        ft.Container(height=6),
        controls_row,
        ft.Container(height=8),
        buttons_row,
        ft.Container(height=8),
        preview_title,
        ft.Container(height=4),
        preview_box
    )

ft.app(target=main)
