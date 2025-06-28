from io import BytesIO
import subprocess
from PIL import Image
import tempfile
import os

class ImageCompressor:
    def __init__(self, image_path=None, image_data=None):
        if image_path is None and image_data is None:
            raise ValueError("Either image_path or image_data must be provided")
            
        self.image_path = image_path
        self.image_data = image_data
        self.temp_files = []
        
    def __del__(self):
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
