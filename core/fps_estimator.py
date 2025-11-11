# core/fps_estimator.py
import pygame
import numpy as np
from datetime import datetime
import math

class FPSEstimator:
    """Estimates the actual frame rate of the display."""
    
    def __init__(self, duration=5.0):
        """
        Args:
            duration: How long to measure frame rate (seconds)
        """
        self.duration = duration
        self.measured_fps = None
    
    def estimate(self, screen, clock):
        """
        Measure the actual frame rate by running a test routine.
        
        Args:
            screen: pygame surface
            clock: Clock object for timing
        
        Returns:
            float: Measured frames per second, or None if cancelled
        """
        font = pygame.font.Font(None, 36)
        pygame_clock = pygame.time.Clock()
        
        frame_data = []
        start_time = datetime.now()
        
        print(f"Measuring frame rate for {self.duration} seconds...")
        
        running = True
        while running:
            # Check for early exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
            
            # Check if duration elapsed
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed >= self.duration:
                running = False
                break
            
            # Log which second we're in
            current_second = math.floor(elapsed)
            frame_data.append(current_second)
            
            # Draw
            screen.fill((50, 50, 50))
            
            text = font.render("Estimating frame rate...", True, (255, 255, 255))
            rect = text.get_rect(center=(400, 250))
            screen.blit(text, rect)
            
            progress_text = font.render(f"{elapsed:.1f} / {self.duration:.1f} seconds", True, (200, 200, 200))
            progress_rect = progress_text.get_rect(center=(400, 300))
            screen.blit(progress_text, progress_rect)
            
            pygame.display.flip()
            
            # No frame rate limiting during measurement
            # (we want to measure actual refresh rate)
        
        # Calculate FPS from collected data
        unique_seconds, counts = np.unique(np.array(frame_data), return_counts=True)
        measured_fps = np.mean(counts)
        
        self.measured_fps = measured_fps
        
        print(f"Measured frame rate: {measured_fps:.2f} Hz")
        print(f"Frame counts per second: {counts}")
        
        return measured_fps