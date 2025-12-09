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
        """Classic cartoon effect - Clean and accurate"""
        # Reduce noise
        img = cv2.medianBlur(img, 5)
        
        # Create edge mask
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        
        # Bilateral filter - preserve edges while smoothing
        color = cv2.bilateralFilter(img, 9, 300, 300)
        
        # Combine color with edges
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        # Convert to RGB
        cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
        return Image.fromarray(cartoon)
    
    def _smooth_cartoon(self, img):
        """Smooth cartoon - Clean and simple"""
        # Apply bilateral filter multiple times for smooth effect
        for i in range(9):
            img = cv2.bilateralFilter(img, 9, 75, 75)
        
        # Simple color quantization
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        k = 9
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        result = centers[labels.flatten()].reshape(img.shape)
        
        # Convert to RGB
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        return Image.fromarray(result)
        
        # Final bilateral filter
        smooth = cv2.bilateralFilter(smooth, d=9, sigmaColor=100, sigmaSpace=100)
        
        # Convert back to RGB
        cartoon = cv2.cvtColor(smooth, cv2.COLOR_BGR2RGB)
        return Image.fromarray(cartoon)
    
    def _pencil_sketch(self, img):
        """Pencil sketch - Artistic drawing"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Denoise
        gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Invert the image
        inv_gray = 255 - gray
        
        # Apply Gaussian blur
        blur = cv2.GaussianBlur(inv_gray, (25, 25), 0)
        
        # Invert blurred image
        inv_blur = 255 - blur
        
        # Create sketch using divide
        sketch = cv2.divide(gray, inv_blur, scale=256.0)
        
        # Enhance contrast
        sketch = cv2.equalizeHist(sketch)
        
        # Add slight texture
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sketch = cv2.filter2D(sketch, -1, kernel * 0.5)
        
        # Convert to RGB
        sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(sketch_rgb)
    
    def _watercolor_effect(self, img):
        """Watercolor painting effect - Clean and artistic"""
        # Bilateral filter for smooth base
        img = cv2.bilateralFilter(img, 9, 75, 75)
        
        # Apply stylization
        result = cv2.stylization(img, sigma_s=60, sigma_r=0.6)
        
        # Slight blur for watercolor feel
        result = cv2.medianBlur(result, 5)
        
        # Convert to RGB
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        return Image.fromarray(result)
    
    def _comic_book_style(self, img):
        """Comic book style - Clean and bold"""
        # Reduce noise
        img = cv2.medianBlur(img, 7)
        
        # Edge detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        
        # Color quantization for comic effect
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        k = 8
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()].reshape(img.shape)
        
        # Bilateral filter
        quantized = cv2.bilateralFilter(quantized, 9, 300, 300)
        
        # Combine with edges
        comic = cv2.bitwise_and(quantized, quantized, mask=edges)
        
        # Convert to RGB
        comic = cv2.cvtColor(comic, cv2.COLOR_BGR2RGB)
        return Image.fromarray(comic)
        
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
