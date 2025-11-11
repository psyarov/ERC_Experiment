# core/gradcpt_stimulus.py
import numpy as np
import random
from glob import glob
from PIL import Image

class StimulusManager:
    """Manages stimulus loading, sequencing, and morphing for GradCPT."""
    
    def __init__(self, config):
        self.config = config
        self.dom_images = []
        self.nondom_images = []
        self.sequence = []
        self.conditions = []
        
        # Load images
        self._load_images()
    
    def _load_images(self):
        """Load and preprocess city and mountain images."""
        print("Loading stimuli...")
        
        # Get file paths
        dom_files = glob(self.config.dom_stim_path)
        nondom_files = glob(self.config.nondom_stim_path)
        
        if not dom_files or not nondom_files:
            raise FileNotFoundError(
                f"Could not find stimulus images. Please ensure images are in:\n"
                f"  {self.config.dom_stim_path}\n"
                f"  {self.config.nondom_stim_path}"
            )
        
        print(f"Found {len(dom_files)} city images and {len(nondom_files)} mountain images")
        
        # Load dominant (city) images
        for filepath in dom_files:
            img = self._load_and_process_image(filepath)
            self.dom_images.append(img)
        
        # Load non-dominant (mountain) images
        for filepath in nondom_files:
            img = self._load_and_process_image(filepath)
            self.nondom_images.append(img)
        
        print(f"Loaded {len(self.dom_images)} processed city images")
        print(f"Loaded {len(self.nondom_images)} processed mountain images")
    
    def _load_and_process_image(self, filepath):
        """
        Load and process a single image.
        - Convert to grayscale
        - Resize to 256x256
        - Apply circular crop
        - Normalize to [-1, 1]
        """
        # Load image
        img = Image.open(filepath)
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Resize to 256x256
        img = img.resize((256, 256), Image.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img, dtype=np.float32)
        
        # Apply circular mask
        img_array = self._apply_circular_mask(img_array)
        
        # Normalize from [0, 255] to [-1, 1]
        img_array = (img_array / 255.0) * 2.0 - 1.0
        
        return img_array
    
    def _apply_circular_mask(self, img):
        """Apply a circular mask to the image."""
        height, width = img.shape
        center_y, center_x = height / 2, width / 2
        radius = min(center_x, center_y)
        
        # Create coordinate arrays
        y, x = np.ogrid[:height, :width]
        
        # Create circular mask
        mask = ((y - center_y) ** 2 + (x - center_x) ** 2) <= radius ** 2
        
        # Apply mask (set outside to middle gray: 127.5 in [0, 255])
        img[~mask] = 127.5
        
        return img
    
    def generate_sequence(self):
        """
        Generate a pseudo-random sequence of stimuli.
        Ensures no consecutive identical images.
        """
        # Create condition labels
        conditions = ['dom'] * self.config.n_dom + ['nondom'] * self.config.n_nondom
        random.shuffle(conditions)
        
        # Initialize sequence
        self.sequence = [None] * len(conditions)
        self.conditions = conditions
        
        # Assign first image
        if conditions[0] == 'dom':
            self.sequence[0] = random.choice(self.dom_images)
        else:
            self.sequence[0] = random.choice(self.nondom_images)
        
        # Assign remaining images (ensuring no consecutive duplicates)
        for i in range(1, len(conditions)):
            new_image = self.sequence[i - 1]
            
            # Keep selecting until we get a different image
            while np.array_equal(new_image, self.sequence[i - 1]):
                if conditions[i] == 'dom':
                    new_image = random.choice(self.dom_images)
                else:
                    new_image = random.choice(self.nondom_images)
            
            self.sequence[i] = new_image
        
        print(f"Generated sequence: {self.config.n_dom} city, {self.config.n_nondom} mountain")
    
    def get_initial_transition(self):
        """
        Get the initial transition from gray to the first image.
        """
        gray = np.zeros((256, 256), dtype=np.float32)  # Middle gray in [-1, 1] space is 0
        return np.linspace(gray, self.sequence[0], self.config.transition_steps, endpoint=False)
    
    def get_transition(self, idx1, idx2):
        """
        Generate a morphing transition between two images in the sequence.
        
        Args:
            idx1: Index of starting image
            idx2: Index of ending image
        
        Returns:
            numpy array of shape (transition_steps, 256, 256) containing the morph sequence
        """
        img1 = self.sequence[idx1]
        img2 = self.sequence[idx2]
        
        # Use numpy's linspace for pixel-by-pixel linear interpolation
        # endpoint=False because we want to exclude the final frame (it becomes the start of next transition)
        transition = np.linspace(img1, img2, self.config.transition_steps, endpoint=False)
        
        return transition