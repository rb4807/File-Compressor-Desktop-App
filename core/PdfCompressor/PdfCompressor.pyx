import os
import tempfile
import zipfile
from io import BytesIO
from PIL import Image
import fitz 
import subprocess

class PdfCompressor:
    def __init__(self):
        """
        Initialize PDF handler with an ImageCompressor instance.
        """
        self.compressor = ImageCompressor(image_data=b'')  # Initialize with empty data
        self.temp_files = []
        
    def __del__(self):
        """Clean up temporary files when the object is deleted."""
        if hasattr(self, 'temp_files'):
            for temp_file in self.temp_files:
                try:
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Failed to delete temporary file {temp_file}: {e}")
    
    def _get_temp_file(self, extension):
        """Create a temporary file with the given extension."""
        temp_file = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        return temp_file.name
    
    def _ensure_pdf_file(self, pdf_path=None, pdf_data=None):
        """
        Ensure we have a PDF file path, creating one from data if needed.
        Returns the path to the PDF file.
        """
        if pdf_path:
            return pdf_path
        elif pdf_data:
            temp_path = self._get_temp_file('.pdf')
            with open(temp_path, 'wb') as f:
                f.write(pdf_data)
            return temp_path
        else:
            raise ValueError("Either pdf_path or pdf_data must be provided")
    
    def _convert_pdf_to_images(self, pdf_path, dpi=200):
        """
        Convert PDF to individual images.
        Returns a list of image file paths.
        """
        pdf_document = fitz.open(pdf_path)
        image_paths = []
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
            
            image_path = self._get_temp_file('.png')
            pix.save(image_path)
            image_paths.append(image_path)
        
        return image_paths
    
    def _compress_images(self, image_paths, output_format='png', quality=85, 
                        resize=None, strip_metadata=True, colors=256, optimize=True):
        """
        Compress a list of images using the image compressor.
        Returns a list of compressed image data (bytes).
        """
        compressed_images = []
        
        for image_path in image_paths:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Create new ImageCompressor instance for each image
            compressor = ImageCompressor(image_data=image_data)
            compressed_data = compressor.process_image(
                output_format=output_format,
                quality=quality,
                resize=resize,
                strip_metadata=strip_metadata,
                colors=colors,
                optimize=optimize
            )
            compressed_images.append(compressed_data)
        
        return compressed_images
    
    def _create_pdf_from_images(self, image_data_list, output_format='png'):
        """
        Combine multiple images into a single PDF.
        Returns PDF data as bytes.
        """
        pdf_buffer = BytesIO()
        
        # Convert all images to PIL Image objects
        images = []
        for img_data in image_data_list:
            img = Image.open(BytesIO(img_data))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
        
        # Save first image as PDF, then append others
        if images:
            images[0].save(
                pdf_buffer,
                format='PDF',
                save_all=True,
                append_images=images[1:]
            )
        
        return pdf_buffer.getvalue()
    
    def _create_zip_from_images(self, image_data_list, output_format='png'):
        """
        Create a zip file containing all images.
        Returns zip data as bytes.
        """
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, img_data in enumerate(image_data_list, start=1):
                zip_file.writestr(
                    f'page_{i}.{output_format}',
                    img_data
                )
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def process_pdf(self, pdf_path=None, pdf_data=None, output_format='pdf', 
               quality=85, resize=None, strip_metadata=True, colors=256, 
               optimize=True, dpi=200):
        """
        Process a PDF by splitting into images, compressing each image, and 
        combining based on output format.
        
        Args:
            pdf_path: Path to input PDF file
            pdf_data: PDF file data as bytes
            output_format: 'pdf' to return PDF, or image format ('png', 'jpg', etc.)
            quality: Quality setting (1-100)
            resize: Optional (width, height) to resize images
            strip_metadata: Whether to remove metadata
            colors: Maximum number of colors
            optimize: Whether to optimize output
            dpi: Resolution for PDF to image conversion
            
        Returns:
            Bytes of the output file (PDF or zip of images)
        """
        # Normalize output format
        output_format = output_format.lower()
        if output_format == 'jpg':
            output_format = 'jpeg'  
        
        input_path = self._ensure_pdf_file(pdf_path, pdf_data)
        
        # Convert PDF to individual images
        image_paths = self._convert_pdf_to_images(input_path, dpi)
        
        # Compress each image
        compressed_images = self._compress_images(
            image_paths,
            output_format='png',  # Always convert to PNG first for quality
            quality=quality,
            resize=resize,
            strip_metadata=strip_metadata,
            colors=colors,
            optimize=optimize
        )
        
        # Create output based on requested format
        if output_format == 'pdf':
            # Convert images back to PDF
            output_data = self._create_pdf_from_images(compressed_images)
        else:
            # If requesting specific image format, convert each image
            if output_format != 'png':
                converted_images = []
                for img_data in compressed_images:
                    # Convert from PNG to requested format
                    img = Image.open(BytesIO(img_data))
                    img_buffer = BytesIO()
                    # Use uppercase format for PIL
                    img.save(img_buffer, format=output_format.upper(), quality=quality)
                    converted_images.append(img_buffer.getvalue())
                compressed_images = converted_images
            
            # Create zip file of images
            output_data = self._create_zip_from_images(compressed_images, output_format)
        
        return output_data
    
    def save_output(self, output_data, output_path):
        """Save the processed output to a file."""
        with open(output_path, 'wb') as f:
            f.write(output_data)

class ImageCompressor:
    def __init__(self, image_path=None, image_data=None):
        if image_path is None and image_data is None:
            raise ValueError("Either image_path or image_data must be provided")
            
        self.image_path = image_path
        self.image_data = image_data
        self.temp_files = []
        
    def __del__(self):
        if hasattr(self, 'temp_files'):
            for temp_file in self.temp_files:
                try:
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Failed to delete temporary file {temp_file}: {e}")
    
    def _get_temp_file(self, extension):
        temp_file = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        return temp_file.name
    
    def _ensure_image_file(self):
        if self.image_path:
            return self.image_path
        elif self.image_data:
            temp_path = self._get_temp_file('.png')
            with open(temp_path, 'wb') as f:
                f.write(self.image_data)
            return temp_path
        return None
    
    def process_image(self, output_format='png', quality=85, resize=None, strip_metadata=True, colors=256, optimize=True):
        input_path = self._ensure_image_file()
        output_path = self._get_temp_file(f'.{output_format}')
        command = ['magick', input_path]
        
        if resize:
            command.extend(['-resize', f'{resize[0]}x{resize[1]}'])
        if strip_metadata:
            command.append('-strip')
        if colors:
            command.extend(['-colors', str(colors)])
        if optimize:
            if output_format.lower() in ['jpg', 'jpeg']:
                command.extend(['-interlace', 'JPEG']) 
        
        command.extend(['-quality', str(quality), output_path])
        
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with open(output_path, 'rb') as f:
                return f.read()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ImageMagick processing failed: {e.stderr.decode()}") from e
    
    def get_pil_image(self, **kwargs):
        image_data = self.process_image(**kwargs)
        return Image.open(BytesIO(image_data))
    
    def save_to_file(self, output_path, **kwargs):
        image_data = self.process_image(**kwargs)
        with open(output_path, 'wb') as f:
            f.write(image_data)