from django.shortcuts import render
import qrcode
from django.http import HttpResponse, HttpResponseBadRequest
from io import BytesIO
import base64
from PIL import Image, ImageDraw
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError




def qr_code_page(request):
    return render(request, 'qrapp/qr_code.html')


# Generate QR Code
# def generate_qr_code(request):
#     qr_code = None  
#     if request.method == "POST":
#         # Get the URL from the form input
#         url = request.POST.get('url', '')

#         # Create a QR code object
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(url)
#         qr.make(fit=True)

#         # Create an image from the QR code
#         img = qr.make_image(fill='black', back_color='white')

#         # Save the image to an in-memory buffer
#         buffer = BytesIO()
#         img.save(buffer, format="PNG")
#         buffer.seek(0)

#         # Encode the image to base64 for embedding in the HTML and storing in session
#         image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

#         # Save the base64-encoded QR image in session to be downloaded later
#         request.session['qr_image'] = image_base64

#         # Pass the base64 encoded image to the template to display it
#         qr_code = image_base64

#     # Render the template with the QR code if generated
#     return render(request, 'qrapp/qr_code.html', {'qr_code': qr_code})


def generate_qr_code(request):
    qr_code = None  
    error_message = None

    if request.method == "POST":
        url = request.POST.get('url', '')

        # Validate the URL
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError:
            error_message = "Please enter a valid URL."

        if not error_message:
            # Create the QR code object with higher error correction
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill='black', back_color='white').convert('RGBA')

            # Create a circular (speech bubble) image
            qr_width, qr_height = img.size
            bubble_size = qr_width // 4  # Make sure the bubble is smaller relative to the QR code
            bubble = Image.new('RGBA', (bubble_size, bubble_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(bubble)
            draw.ellipse((0, 0, bubble_size, bubble_size), fill=(255, 255, 255, 255))  # White circle

            # Get the size of the QR code and calculate the position for the bubble
            bubble_position = ((qr_width - bubble_size) // 2, (qr_height - bubble_size) // 2)

            # Paste the bubble image onto the QR code image
            img.paste(bubble, bubble_position, bubble)

            # Save the final image to an in-memory buffer
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # Encode the image to base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Save the base64-encoded QR image in session to be downloaded later
            request.session['qr_image'] = image_base64

            # Pass the base64 encoded image to the template to display it
            qr_code = image_base64

    return render(request, 'qrapp/qr_code.html', {'qr_code': qr_code, 'error_message': error_message})


# New view to handle QR code download
def download_qr_code(request):
    # Retrieve the base64-encoded QR code from session
    qr_image_base64 = request.session.get('qr_image', None)
    
    if not qr_image_base64:
        return HttpResponseBadRequest("QR Code not generated yet.")

    # Decode the base64-encoded image back to bytes
    qr_image_bytes = base64.b64decode(qr_image_base64)

    # Send the QR code as a downloadable PNG file
    response = HttpResponse(qr_image_bytes, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="qr_code.png"'
    
    return response

