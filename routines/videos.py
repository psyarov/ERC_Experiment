import pygame
import numpy as np

def videos(screen, clock):
    """
    Social media routine with 20-minute video scrolling period.
    
    Args:
        screen: pygame display surface
        clock: Clock object for timing
    
    Returns:
        True: if routine completed successfully
        None: if routine was exited with ESC or window closed
    """
    # Colors
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    BLACK = (0, 0, 0)
    
    # Font setup
    pygame.font.init()
    font_medium = pygame.font.Font(None, 36)
    
    screen_width, screen_height = screen.get_size()
    
    # ========== INSTRUCTION SCREEN ==========
    print("=" * 50)
    print("SOCIAL MEDIA ROUTINE - INSTRUCTIONS")
    print("=" * 50)
    
    instruction_lines = [
        "In the next 20 minutes, please take your phone and scroll",
        "the short-form videos on the chosen application.",
        "",
        "Please, refrain from interacting with the content or creators.",
        "Simply watch and scroll at your own pace.",
        "",
        "You will hear a sound whenever the time is over.",
        "",
        "Press SPACE to begin."
    ]
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed during social media routine instructions")
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC pressed during social media routine instructions")
                    return None
                elif event.key == pygame.K_SPACE:
                    waiting = False
        
        screen.fill(GRAY)
        
        # Render instruction text
        y_offset = screen_height // 2 - 170
        for line in instruction_lines:
            text_surface = font_medium.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 45
        
        pygame.display.flip()
    
    print("Instructions acknowledged - starting social media period")
    
    # ========== SOCIAL MEDIA PERIOD (20 minutes) ==========
    print("Social media period started (20 minutes)...")
    
    start_time = clock.get_time()
    #video_duration = 1200.0  # 20 minutes = 1200 seconds
    video_duration = 120.0 # For testing, set to 120 seconds
    
    # Black screen during video watching
    screen.fill(BLACK)
    pygame.display.flip()
    
    while clock.get_time() - start_time < video_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed during social media period")
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC pressed during social media period")
                    return None
        
        # Keep the screen black
        pygame.time.wait(100)  # Small delay to reduce CPU usage
    
    print("Social media period complete (20 minutes elapsed)")
    
    # ========== PLAY ALARM SOUND ==========
    print("Playing alarm sound...")
    
    # Create a simple beep sound
    # This generates a 440 Hz tone for 0.5 seconds
    sample_rate = 22050
    #duration = 0.5  # seconds
    duration = 1.0 # For testing, set to 1 second
    frequency = 440  # Hz (A4 note)
    
    # Generate the sound
    n_samples = int(sample_rate * duration)
    buffer = np.sin(2 * np.pi * frequency * np.linspace(0, duration, n_samples))
    # Fade in/out to avoid clicks
    fade_samples = int(sample_rate * 0.01)  # 10ms fade
    buffer[:fade_samples] *= np.linspace(0, 1, fade_samples)
    buffer[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    # Convert to 16-bit
    buffer = (buffer * 32767).astype(np.int16)
    # Make stereo
    stereo_buffer = np.column_stack((buffer, buffer))
    
    # Initialize mixer if not already initialized
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=sample_rate, size=-16, channels=2)
    
    # Play the sound
    sound = pygame.mixer.Sound(buffer=stereo_buffer)
    sound.play()
    
    # Wait for sound to finish
    while pygame.mixer.get_busy():
        pygame.time.wait(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
    
    print("Alarm sound played")
    print("Social media routine complete")
    print("=" * 50)
    
    return True