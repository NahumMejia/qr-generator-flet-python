import flet as ft
import qrcode
from io import BytesIO
import base64

def main(page: ft.Page):
    page.title = "QR Code Generator"
    page.scroll = None
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Available colors for QR codes (name and hex value)
    colors = {
        "black": "#000000",
        "white": "#FFFFFF",
        "red": "#FF0000",
        "green": "#008000",
        "blue": "#0000FF",
        "yellow": "#FFFF00",
        "orange": "#FFA500",
        "purple": "#800080",
        "pink": "#FFC0CB",
        "brown": "#A52A2A",
        "gray": "#808080",
        "cyan": "#00FFFF",
        "magenta": "#FF00FF",
        "lime": "#00FF00",
        "navy": "#000080",
        "teal": "#008080",
        "maroon": "#800000",
        "olive": "#808000",
        "silver": "#C0C0C0",
        "gold": "#FFD700"
    }

    # Variable to store the generated image
    current_qr_image = None

    # Compact title text
    title_text = ft.Text(
        value="QR Code Generator", 
        size=40, 
        weight=ft.FontWeight.W_100
    )
    
    # Compact input field for URL
    url_input = ft.TextField(
        label="URL", 
        width=350,
        hint_text="https://example.com",
        value="https://example.com",
        dense=True
    )
    
    # Dropdown for background color
    background_color_dropdown = ft.Dropdown(
        label="Background",
        width=150,
        value="white",
        dense=True,
        options=[ft.dropdown.Option(key=color_name, text=color_name.capitalize()) 
                 for color_name in colors.keys()]
    )
    
    # Dropdown for code color
    code_color_dropdown = ft.Dropdown(
        label="Code color",
        width=150,
        value="black",
        dense=True,
        options=[ft.dropdown.Option(key=color_name, text=color_name.capitalize()) 
                 for color_name in colors.keys()]
    )
    
    # Dropdown for border size
    border_dropdown = ft.Dropdown(
        label="Border",
        width=120,
        value="4",
        dense=True,
        options=[
            ft.dropdown.Option(key="1", text="1"),
            ft.dropdown.Option(key="2", text="2"),
            ft.dropdown.Option(key="3", text="3"),
            ft.dropdown.Option(key="4", text="4"),
            ft.dropdown.Option(key="5", text="5"),
            ft.dropdown.Option(key="6", text="6"),
            ft.dropdown.Option(key="8", text="8"),
        ]
    )
    
    # "QR Preview" legend text, compact
    preview_title = ft.Text(
        "QR Preview",
        size=18,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    # Initial preview text
    preview_content = ft.Text(
        "Generate to see the QR code", 
        size=14, 
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.GREY_600
    )
    
    preview_box = ft.Container(
        content=preview_content,
        width=250,
        height=250,
        border=ft.border.all(2, ft.Colors.GREY_400),
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.GREY_100
    )
    
    def generate_qr(e):
        nonlocal current_qr_image
        
        url = url_input.value
        if not url:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter a URL"))
            page.snack_bar.open = True
            page.update()
            return
        
        # Validate that colors are not the same
        if code_color_dropdown.value == background_color_dropdown.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Code color and background color must be different!")
            )
            page.snack_bar.open = True
            page.update()
            return
        
        try:
            # Get hex colors
            fill_color = colors[code_color_dropdown.value]
            back_color = colors[background_color_dropdown.value]
            border_size = int(border_dropdown.value)
            
            print(f"Generating QR with fill_color={fill_color}, back_color={back_color}, border={border_size}")
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=border_size,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            # Generate image with selected colors using hex codes
            img = qr.make_image(
                fill_color=fill_color,
                back_color=back_color
            )
            
            # Save the image for later download
            current_qr_image = img
            
            # Convert to base64 to display in Flet
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            
            print(f"Image generated, base64 length: {len(img_base64)}")
            
            # Create new image and replace content
            new_image = ft.Image(
                src_base64=img_base64,
                width=230,
                height=230,
                fit=ft.ImageFit.CONTAIN
            )
            
            preview_box.content = new_image
            
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"QR generated: {code_color_dropdown.value} on {background_color_dropdown.value}")
            )
            page.snack_bar.open = True
            page.update()
            
        except Exception as ex:
            print(f"Error generating QR: {ex}")
            import traceback
            traceback.print_exc()
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"))
            page.snack_bar.open = True
            page.update()
    
    def download_qr(e):
        if current_qr_image is None:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please generate a QR code first"))
            page.snack_bar.open = True
            page.update()
            return
        
        try:
            # Save the file
            filename = "qrcode.png"
            current_qr_image.save(filename)
            
            print(f"QR Code saved as {filename}")
            
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"QR Code saved as {filename}"),
                duration=3000
            )
            page.snack_bar.open = True
            page.update()
            
        except Exception as ex:
            print(f"Error saving: {ex}")
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error saving: {str(ex)}"))
            page.snack_bar.open = True
            page.update()
    
    # Compact buttons
    generate_button = ft.ElevatedButton(
        text="GENERATE",
        icon=ft.Icons.QR_CODE,
        width=180,
        on_click=generate_qr,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )
    
    download_button = ft.ElevatedButton(
        text="DOWNLOAD", 
        icon=ft.Icons.DOWNLOAD,
        width=180,
        on_click=download_qr,
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE
    )
    
    # Layout in rows for space 
    page.add(
        title_text,
        ft.Container(height=5),
        url_input,
        ft.Container(height=10),
        ft.Row(
            controls=[background_color_dropdown, code_color_dropdown, border_dropdown],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        ft.Container(height=10),
        ft.Row(
            controls=[generate_button, download_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        ft.Container(height=15),
        preview_title,
        ft.Container(height=5),
        preview_box
    )

ft.app(target=main)
