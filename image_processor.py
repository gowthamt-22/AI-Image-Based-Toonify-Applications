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
        - oil: Oil painting effect
        - pop: Pop art style
        - anime: Anime style effect
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
        elif style == 'oil':
            return self._oil_painting(img)
        elif style == 'pop':
            return self._pop_art(img)
        elif style == 'anime':
            return self._anime_style(img)
        else:
            return self._classic_cartoon(img)
    
    def _classic_cartoon(self, img):
        """Classic cartoon - A refined, beautiful cartoon look with great detail"""
        # Step 1: Enhance quality for a better base
        img = self.enhance_quality(img)

        # Step 2: Edge-preserving filter for initial smoothing
        smooth = cv2.edgePreservingFilter(img, flags=1, sigma_s=60, sigma_r=0.5)
        
        # Step 3: Multiple bilateral filtering passes for a polished look
        for _ in range(5):
            smooth = cv2.bilateralFilter(smooth, d=9, sigmaColor=80, sigmaSpace=80)
        
        # Step 4: Advanced edge detection for fine lines
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 9, 4)
        
        # Step 5: Color quantization with more colors for a detailed, vibrant palette
        data = smooth.reshape((-1, 3)).astype(np.float32)
        k = 40  # Increased colors for a richer, more beautiful output
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.2)
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()].reshape(smooth.shape)
        
        # Step 6: Fine-tuned saturation and brightness for a lively feel
        hsv = cv2.cvtColor(quantized, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.4, 0, 255) # Enhanced saturation
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.15, 0, 255) # Subtle brightness
        cartoon = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 7: Combine color with sharp edges
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(cartoon, edges_bgr)
        
        # Step 8: Final detail enhancement for a stunning finish
        cartoon = cv2.detailEnhance(cartoon, sigma_s=15, sigma_r=0.2)
        
        return Image.fromarray(cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB))

    def _smooth_cartoon(self, img):
        """Smooth cartoon - Ultra-clean, flat colors with bold, defined edges"""
        # Step 1: Heavy bilateral filtering for an extremely smooth base
        smooth = img.copy()
        for _ in range(10):
            smooth = cv2.bilateralFilter(smooth, d=10, sigmaColor=100, sigmaSpace=100)
        
        # Step 2: Detect edges clearly on the original image for sharpness
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 8)
        
        # Step 3: Color quantization with fewer colors for a very flat, graphic look
        data = smooth.reshape((-1, 3)).astype(np.float32)
        k = 10  # Reduced colors for a flatter, more graphic style
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 150, 0.2)
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()].reshape(smooth.shape)
        
        # Step 4: Boost saturation for a vibrant, punchy look
        hsv = cv2.cvtColor(quantized, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.8, 0, 255)  # Strong saturation
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)  # Boost brightness
        cartoon = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 5: Combine with edges
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(cartoon, edges_bgr)
        
        return Image.fromarray(cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB))
    
    def _pencil_sketch(self, img):
        """Pencil sketch - Artistic black and white sketch"""
        # Step 1: Enhance quality
        img = self.enhance_quality(img)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Invert
        inverted = 255 - gray
        
        # Gaussian blur for a softer look
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        
        # Dodge blend
        def dodge_blend(front, back):
            result = back * 255.0 / (255.0 - front + 1e-6) # Add epsilon for stability
            result[result > 255] = 255
            result[back == 255] = 255
            return result.astype('uint8')
        
        sketch = dodge_blend(blurred, gray)
        
        # Adjust contrast for a more balanced look
        sketch = cv2.equalizeHist(sketch)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        sketch = clahe.apply(sketch)
        
        # Scale for better definition
        sketch = cv2.convertScaleAbs(sketch, alpha=1.2, beta=-10)
        
        # Sharpen for crisp lines
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        sketch = cv2.filter2D(sketch, -1, kernel)
        
        # Convert to RGB
        sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(sketch_rgb)
    
    def _watercolor_effect(self, img):
        """Watercolor - A beautiful, artistic watercolor painting with a 'wet' feel"""
        # Step 1: Use stylization for a strong painterly base
        watercolor = cv2.stylization(img, sigma_s=150, sigma_r=0.45)
        
        # Step 2: Moderate color boost for a rich, not oversaturated, palette
        hsv = cv2.cvtColor(watercolor, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.8, 0, 255)  # Rich saturation
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
        watercolor = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 3: Heavy bilateral filtering to blend colors like wet paint
        for _ in range(8):
            watercolor = cv2.bilateralFilter(watercolor, d=10, sigmaColor=120, sigmaSpace=120)
        
        # Step 4: Add detail enhancement to bring back some texture
        watercolor = cv2.detailEnhance(watercolor, sigma_s=20, sigma_r=0.3)
        
        # Step 5: Final color and contrast adjustment for a masterpiece look
        watercolor = cv2.convertScaleAbs(watercolor, alpha=1.2, beta=10)
        
        return Image.fromarray(cv2.cvtColor(watercolor, cv2.COLOR_BGR2RGB))

    def _comic_book_style(self, img):
        """Comic book - Bold, graphic style with thick lines and vibrant colors"""
        # Step 1: Heavy posterization for a classic comic book color palette
        div = 48  # Fewer colors for a more dramatic, graphic effect
        quantized = img // div * div + div // 2
        
        # Step 2: Bilateral filtering for smooth color areas
        for _ in range(6):
            quantized = cv2.bilateralFilter(quantized, d=9, sigmaColor=90, sigmaSpace=90)
        
        # Step 3: Strong saturation boost for that classic comic vibrancy
        hsv = cv2.cvtColor(quantized, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 2.2, 0, 255)  # Very vibrant
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.25, 0, 255)
        quantized = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 4: Create thick, bold black outlines
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
        
        # Thicken edges dramatically
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=2)
        
        # Step 5: Combine colors and outlines
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        comic = cv2.bitwise_and(quantized, edges_bgr)
        
        return Image.fromarray(cv2.cvtColor(comic, cv2.COLOR_BGR2RGB))

    def _oil_painting(self, img):
        """Oil painting - A rich, textured oil paint effect with visible brush strokes"""
        # Step 1: Use the dedicated oil painting function with larger parameters
        oil = cv2.xphoto.oilPainting(img, 10, 1, cv2.COLOR_BGR2Lab) # Use Lab space for better results
        
        # Step 2: Boost colors for a rich, deep palette
        hsv = cv2.cvtColor(oil, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.9, 0, 255)  # Deep, rich saturation
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
        oil = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 3: Enhance details to simulate brush stroke texture
        oil = cv2.detailEnhance(oil, sigma_s=10, sigma_r=0.3)
        
        # Step 4: Sharpen to define the "edges" of the brush strokes
        kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
        oil = cv2.filter2D(oil, -1, kernel)
        
        # Step 5: Final contrast adjustment
        oil = cv2.convertScaleAbs(oil, alpha=1.2, beta=10)
        
        return Image.fromarray(cv2.cvtColor(oil, cv2.COLOR_BGR2RGB))

    def _pop_art(self, img):
        """Pop art - Ultra-vibrant, high-contrast Andy Warhol style"""
        # Step 1: Extreme posterization for a very limited, bold color palette
        div = 96  # Very aggressive posterization
        quantized = img // div * div + div // 2
        
        # Step 2: Massive saturation boost for iconic pop art colors
        hsv = cv2.cvtColor(quantized, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 3.5, 0, 255)  # Extremely vibrant
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.4, 0, 255)  # Very bright
        quantized = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 3: Heavy smoothing for perfectly flat color blocks
        for _ in range(10):
            quantized = cv2.bilateralFilter(quantized, d=9, sigmaColor=150, sigmaSpace=150)
        
        # Step 4: High contrast to make the colors pop
        quantized = cv2.convertScaleAbs(quantized, alpha=1.6, beta=30)
        
        # Step 5: Detect and add strong, clean edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 30, 100)
        edges = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # Invert edges and combine
        edges_bgr = 255 - edges_bgr
        pop = cv2.bitwise_and(quantized, edges_bgr)
        
        return Image.fromarray(cv2.cvtColor(pop, cv2.COLOR_BGR2RGB))

    def _anime_style(self, img):
        """Anime style - A clean, vibrant Japanese animation look with cel-shading"""
        # Step 1: Enhance quality for a sharp base
        img = self.enhance_quality(img)

        # Step 2: Heavy bilateral filtering for that smooth, airbrushed look
        anime = img.copy()
        for _ in range(8):
            anime = cv2.bilateralFilter(anime, d=9, sigmaColor=90, sigmaSpace=90)
        
        # Step 3: Strong, vibrant saturation boost, characteristic of anime
        hsv = cv2.cvtColor(anime, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 2.0, 0, 255) # Strong, clean saturation
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.3, 0, 255)
        anime = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 4: Color quantization for a cel-shaded palette
        data = anime.reshape((-1, 3)).astype(np.float32)
        k = 14  # A good number of colors for anime shading
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.2)
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
        centers = np.uint8(centers)
        anime = centers[labels.flatten()].reshape(anime.shape)
        
        # Step 5: Create very clean, thin, and sharp outlines
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 3)
        
        # Thin the edges for a delicate anime line art style
        kernel = np.ones((1, 1), np.uint8)
        edges = cv2.erode(edges, kernel, iterations=1)
        
        # Step 6: Combine colors and line art
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        anime = cv2.bitwise_and(anime, edges_bgr)
        
        # Step 7: Final brightness and contrast for a polished look
        anime = cv2.convertScaleAbs(anime, alpha=1.15, beta=15)
        
        return Image.fromarray(cv2.cvtColor(anime, cv2.COLOR_BGR2RGB))
    
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
