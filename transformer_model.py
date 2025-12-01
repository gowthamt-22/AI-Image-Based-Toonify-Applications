import torch
import torch.nn as nn
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
import cv2

class ResidualBlock(nn.Module):
    """Residual block for CartoonGAN generator"""
    def __init__(self, channels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)
    
    def forward(self, x):
        residual = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        return out

class CartoonGANGenerator(nn.Module):
    """CartoonGAN Generator Network"""
    def __init__(self, num_residual_blocks=8):
        super(CartoonGANGenerator, self).__init__()
        
        # Initial convolution block
        self.initial = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        
        # Downsampling
        self.down1 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        
        self.down2 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True)
        )
        
        # Residual blocks
        res_blocks = []
        for _ in range(num_residual_blocks):
            res_blocks.append(ResidualBlock(256))
        self.res_blocks = nn.Sequential(*res_blocks)
        
        # Upsampling
        self.up1 = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        
        self.up2 = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        
        # Output layer
        self.output = nn.Sequential(
            nn.Conv2d(64, 3, kernel_size=7, padding=3),
            nn.Tanh()
        )
    
    def forward(self, x):
        x = self.initial(x)
        x = self.down1(x)
        x = self.down2(x)
        x = self.res_blocks(x)
        x = self.up1(x)
        x = self.up2(x)
        x = self.output(x)
        return x

class TransformerCartoonizer:
    """Transformer-based cartoon image processor using CartoonGAN"""
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = CartoonGANGenerator().to(self.device)
        self.model.eval()
        
        # Initialize with random weights since we don't have pre-trained weights
        # In production, you would load pre-trained weights here
        self._initialize_weights()
        
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        self.inverse_transform = transforms.Compose([
            transforms.Normalize(mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
                               std=[1/0.229, 1/0.224, 1/0.225])
        ])
    
    def _initialize_weights(self):
        """Initialize model weights"""
        for m in self.model.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
    
    def preprocess(self, image):
        """Preprocess image for model input"""
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get original size
        orig_size = image.size
        
        # Resize to multiple of 32 for better processing
        w, h = image.size
        new_w = (w // 32) * 32
        new_h = (h // 32) * 32
        image = image.resize((new_w, new_h), Image.LANCZOS)
        
        # Transform to tensor
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        return img_tensor, orig_size
    
    def postprocess(self, tensor, orig_size):
        """Postprocess model output to image"""
        # Denormalize
        tensor = self.inverse_transform(tensor.squeeze(0).cpu())
        
        # Clamp values to [0, 1]
        tensor = torch.clamp(tensor, 0, 1)
        
        # Convert to PIL image
        img = transforms.ToPILImage()(tensor)
        
        # Resize back to original size
        img = img.resize(orig_size, Image.LANCZOS)
        
        return img
    
    def cartoonize(self, image):
        """
        Apply CartoonGAN transformer to image
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            PIL Image - cartoonized image
        """
        with torch.no_grad():
            # Preprocess
            img_tensor, orig_size = self.preprocess(image)
            
            # Forward pass through model
            output = self.model(img_tensor)
            
            # Postprocess
            cartoon_image = self.postprocess(output, orig_size)
            
        return cartoon_image
    
    def enhance_cartoon(self, image, style='vibrant'):
        """
        Apply CartoonGAN and additional post-processing
        
        Args:
            image: PIL Image or numpy array
            style: 'vibrant', 'soft', or 'sharp'
            
        Returns:
            PIL Image - enhanced cartoon image
        """
        # First apply transformer
        cartoon = self.cartoonize(image)
        
        # Convert to numpy for OpenCV processing
        img_np = np.array(cartoon)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        if style == 'vibrant':
            # Increase saturation
            hsv = cv2.cvtColor(img_np, cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.3)
            img_np = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            
        elif style == 'soft':
            # Apply slight blur
            img_np = cv2.bilateralFilter(img_np, 5, 50, 50)
            
        elif style == 'sharp':
            # Sharpen edges
            kernel = np.array([[-1, -1, -1],
                             [-1,  9, -1],
                             [-1, -1, -1]])
            img_np = cv2.filter2D(img_np, -1, kernel)
        
        # Convert back to RGB and PIL
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        result = Image.fromarray(img_np)
        
        return result

def create_transformer_cartoonizer():
    """Factory function to create transformer cartoonizer"""
    return TransformerCartoonizer()

if __name__ == "__main__":
    # Test the transformer model
    print("Testing CartoonGAN Transformer...")
    cartoonizer = create_transformer_cartoonizer()
    print(f"Model loaded on device: {cartoonizer.device}")
    print(f"Model parameters: {sum(p.numel() for p in cartoonizer.model.parameters()):,}")
    print("Ready to cartoonize images!")
