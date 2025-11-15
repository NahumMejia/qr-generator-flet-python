import flet as ft
import qrcode
from io import BytesIO
import base64

def main(page: ft.Page):
    page.title = "QR Code Generator"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 8

    colors = {
        "black": "#000000", "white": "#FFFFFF", "red": "#FF0000",
        "green": "#008000", "blue": "#0000FF", "yellow": "#FFFF00",
        "orange": "#FFA500", "purple": "#800080", "pink": "#FFC0CB",
        "brown": "#A52A2A", "gray": "#808080", "cyan": "#00FFFF",
        "magenta": "#FF00FF", "lime": "#00FF00", "navy": "#000080",
        "teal": "#008080", "maroon": "#800000", "olive": "#808000",
        "silver": "#C0C0C0", "gold": "#FFD700"
    }

    current_qr_base64 = None
    current_qr_image = None

    # File save handler for desktop
    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path and current_qr_image:
            try:
                current_qr_image.save(e.path)
                show_snackbar("QR Code saved!")
            except Exception as ex:
                show_snackbar(f"Error: {str(ex)}")

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)

    def show_snackbar(message):
        page.snack_bar = ft.SnackBar(content=ft.Text(message))
        page.snack_bar.open = True
        page.update()

    # UI Components
    logo_image = ft.Image(src="https://iili.io/K4J8eKF.png", width=120, height=120, fit=ft.ImageFit.CONTAIN)
    title_text = ft.Text("QR Code Generator", size=20, weight=ft.FontWeight.W_100)
    url_input = ft.TextField(label="URL", width=300, hint_text="https://example.com", dense=True, text_size=12)
    
    dropdown_options = [ft.dropdown.Option(key=k, text=k.capitalize()) for k in colors.keys()]
    background_color_dropdown = ft.Dropdown(label="Background", width=120, value="white", dense=True, text_size=12, options=dropdown_options)
    code_color_dropdown = ft.Dropdown(label="Code color", width=120, value="black", dense=True, text_size=12, options=dropdown_options)
    border_dropdown = ft.Dropdown(
        label="Border", width=100, value="4", dense=True, text_size=12,
        options=[ft.dropdown.Option(key=str(i), text=str(i)) for i in [1,2,3,4,5,6,8]]
    )
    
    preview_title = ft.Text("QR Preview", size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    preview_content = ft.Text("Generate to see the QR code", size=12, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY_600)
    preview_box = ft.Container(
        content=preview_content, width=110, height=110,
        border=ft.border.all(2, ft.Colors.GREY_400),
        alignment=ft.alignment.center, bgcolor=ft.Colors.GREY_100
    )
    
    def generate_qr(e):
        nonlocal current_qr_base64, current_qr_image
        
        if not url_input.value:
            show_snackbar("Please enter a URL")
            return
        
        if code_color_dropdown.value == background_color_dropdown.value:
            show_snackbar("Code color and background color must be different!")
            return
        
        try:
            # Generate QR code with selected colors
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, 
                               box_size=10, border=int(border_dropdown.value))
            qr.add_data(url_input.value)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color=colors[code_color_dropdown.value], 
                               back_color=colors[background_color_dropdown.value])
            current_qr_image = img
            
            # Convert to base64 for display
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            current_qr_base64 = base64.b64encode(buffer.read()).decode()
            
            preview_box.content = ft.Image(src_base64=current_qr_base64, width=170, height=170, fit=ft.ImageFit.CONTAIN)
            show_snackbar(f"QR generated: {code_color_dropdown.value} on {background_color_dropdown.value}")
            
        except Exception as ex:
            show_snackbar(f"Error: {str(ex)}")
    
    def download_qr(e):
        if current_qr_base64 is None:
            show_snackbar("Please generate a QR code first")
            return
        
        # Desktop: FilePicker
        save_file_dialog.save_file(dialog_title="Save QR Code", file_name="qrcode.png",
                                  file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["png"])
    
    generate_button = ft.ElevatedButton("GENERATE", icon=ft.Icons.QR_CODE, width=150, height=35, 
                                       on_click=generate_qr, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    download_button = ft.ElevatedButton("DOWNLOAD", icon=ft.Icons.DOWNLOAD, width=150, height=35,
                                       on_click=download_qr, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
    
    # Layout
    page.add(
        logo_image, title_text, ft.Container(height=5), url_input, ft.Container(height=8),
        ft.Row([background_color_dropdown, code_color_dropdown, border_dropdown], 
               alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        ft.Container(height=8),
        ft.Row([generate_button, download_button], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        ft.Container(height=10), preview_title, ft.Container(height=5), preview_box
    )

ft.app(target=main)