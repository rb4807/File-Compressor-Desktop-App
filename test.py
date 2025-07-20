from core.ImageCompressor.ImageCompressor import ImageCompressor
from core.PdfCompressor.PdfCompressor import PdfCompressor

processor = ImageCompressor(image_path='input.jpg')
processed_data = processor.process_image(
    output_format='jpg', 
    quality=90,
    resize=(800, 600),
    colors=128
)

# Save the result
with open('output.jpg', 'wb') as f:
    f.write(processed_data)

pdf_handler = PdfCompressor()

# From PDF data to images (JPG)
with open('input.pdf', 'rb') as f:
    pdf_data = f.read()

images_zip = pdf_handler.process_pdf(
    pdf_data=pdf_data,
    output_format='jpg',
    quality=85
)
pdf_handler.save_output(images_zip, 'images.zip')