import cv2
import numpy as np
from PIL import Image
import io

class ImageProcessor:
    """Handles all image processing and cartoon effect generation"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    
    def enhance_quality(self, img):
        """Enhance image quality using advanced techniques"""
        # Convert to LAB color space for better processing
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        enhanced_lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        # Denoise while preserving edges
        enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
        
        # Sharpen
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        enhanced = cv2.filter2D(enhanced, -1, kernel)
        
        return enhanced
    
    def validate_image(self, image_file):
        """Validate uploaded image file"""
        try:
            img = Image.open(image_file)
            return True, img
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    def convert_to_cartoon(self, image, style='classic'):
        """
        Convert image to cartoon using different styles
        
        Styles:
        - classic: Traditional cartoon with edge detection
        - smooth: Smooth cartoon with bilateral filtering
        - pencil: Pencil sketch effect
        - watercolor: Watercolor painting effect
        - comic: Comic book style with strong edges
        """
        # Convert PIL to OpenCV format
        img = np.array(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        if style == 'classic':
            return self._classic_cartoon(img)
        elif style == 'smooth':
            return self._smooth_cartoon(img)
        elif style == 'pencil':
            return self._pencil_sketch(img)
        elif style == 'watercolor':
            return self._watercolor_effect(img)
        elif style == 'comic':
            return self._comic_book_style(img)
        else:
            return self._classic_cartoon(img)
    
    def _classic_cartoon(self, img):
        """Classic cartoon effect with edge detection"""
        # Enhance image quality first
        img = self.enhance_quality(img)
        
        # Apply bilateral filter for smoothing while preserving edges
        color = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply median blur
        gray = cv2.medianBlur(gray, 7)
        
        # Detect edges using adaptive threshold
        edges = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=9,
            C=2
        )
        
        # Combine color and edges
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        # Convert back to RGB
        cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
        return Image.fromarray(cartoon)
    
    def _smooth_cartoon(self, img):
        """Smooth cartoon with multiple bilateral filters"""
        # Enhance image quality first
        img = self.enhance_quality(img)
        
        # Apply bilateral filter multiple times
        for _ in range(3):
            img = cv2.bilateralFilter(img, d=9, sigmaColor=80, sigmaSpace=80)
        
        # Quantize colors to reduce color palette
        div = 64
        img = img // div * div + div // 2
        
        # Convert back to RGB
        cartoon = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(cartoon)
    
    def _pencil_sketch(self, img):
        """Pencil sketch effect"""
        # Enhance image quality first
        img = self.enhance_quality(img)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Invert grayscale
        inv_gray = 255 - gray
        
        # Apply Gaussian blur
        blur = cv2.GaussianBlur(inv_gray, (21, 21), 0)
        
        # Invert blurred image
        inv_blur = 255 - blur
        
        # Divide grayscale by inverted blurred image
        sketch = cv2.divide(gray, inv_blur, scale=256.0)
        
        # Convert to RGB for display
        sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(sketch_rgb)
    
    def _watercolor_effect(self, img):
        """Watercolor painting effect"""
        # Enhance image quality first
        img = self.enhance_quality(img)
        
        # Apply bilateral filter for smoothing
        color = cv2.bilateralFilter(img, d=9, sigmaColor=90, sigmaSpace=90)
        
        # Apply median blur for artistic effect
        color = cv2.medianBlur(color, 15)
        
        # Reduce color palette
        div = 32
        color = color // div * div + div // 2
        
        # Apply slight blur for watercolor feel
        watercolor = cv2.GaussianBlur(color, (5, 5), 0)
        
        # Convert back to RGB
        watercolor = cv2.cvtColor(watercolor, cv2.COLOR_BGR2RGB)
        return Image.fromarray(watercolor)
    
    def _comic_book_style(self, img):
        """Comic book style with strong edges"""
        # Enhance image quality first
        img = self.enhance_quality(img)
        
        # Apply bilateral filter
        color = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
        
        # Quantize colors more aggressively
        div = 64
        color = color // div * div + div // 2
        
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        
        # Apply median blur
        gray = cv2.medianBlur(gray, 5)
        
        # Detect edges with stronger threshold
        edges = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=5,
            C=2
        )
        
        # Thicken edges
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.erode(edges, kernel, iterations=1)
        
        # Combine color and edges
        comic = cv2.bitwise_and(color, color, mask=edges)
        
        # Convert back to RGB
        comic = cv2.cvtColor(comic, cv2.COLOR_BGR2RGB)
        return Image.fromarray(comic)
    
    def adjust_brightness(self, image, factor=1.0):
        """Adjust image brightness"""
        img_array = np.array(image)
        img_array = np.clip(img_array * factor, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)
    
    def adjust_contrast(self, image, factor=1.0):
        """Adjust image contrast"""
        img_array = np.array(image, dtype=np.float32)
        mean = img_array.mean()
        img_array = mean + factor * (img_array - mean)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)
    
    def adjust_image(self, image, brightness=1.0, contrast=1.0, saturation=1.0, sharpness=1.0):
        """Apply multiple adjustments to image"""
        from PIL import ImageEnhance
        
        # Convert to PIL if needed
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        
        # Apply brightness
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness)
        
        # Apply contrast
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast)
        
        # Apply saturation (color)
        if saturation != 1.0:
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(saturation)
        
        # Apply sharpness
        if sharpness != 1.0:
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(sharpness)
        
        return image
    
    def resize_image(self, image, max_size=1024):
        """Resize image while maintaining aspect ratio"""
        width, height = image.size
        
        if width > max_size or height > max_size:
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))
            
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image
    
    def image_to_bytes(self, image, format='PNG'):
        """Convert PIL Image to bytes for download"""
        buf = io.BytesIO()
        image.save(buf, format=format)
        buf.seek(0)
        return buf.getvalue()
