import pygame

def rest(screen, clock):
    """
    Rest routine with 5-minute relaxation period and gradual color transition.
    
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
    GREEN = (0, 200, 0)
    YELLOW = (200, 200, 0)
    
    # Font setup
    pygame.font.init()
    font_medium = pygame.font.Font(None, 36)
    
    screen_width, screen_height = screen.get_size()
    
    # ========== INSTRUCTION SCREEN ==========
    print("=" * 50)
    print("REST ROUTINE - INSTRUCTIONS")
    print("=" * 50)
    
    instruction_lines = [
        "In the next minutes, please relax and let your mind wander.",
        "While doing so, please try to keep your eyes focused",
        "on the dot on the desk.",
        "",
        "The screen will gradually turn yellow as the time runs out.",
        "The next task will commence automatically.",
        "",
        "Press SPACE to continue and just relax."
    ]
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed during rest routine instructions")
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC pressed during rest routine instructions")
                    return None
                elif event.key == pygame.K_SPACE:
                    waiting = False
        
        screen.fill(GRAY)
        
        # Render instruction text
        y_offset = screen_height // 2 - 150
        for line in instruction_lines:
            text_surface = font_medium.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 45
        
        pygame.display.flip()
    
    print("Instructions acknowledged - starting rest period")
    
    # ========== REST PERIOD (5 minutes with gradual green to yellow) ==========
    print("Rest period started (5 minutes)...")
    
    start_time = clock.get_time()
    rest_duration = 300.0  # 5 minutes = 300 seconds
    
    while clock.get_time() - start_time < rest_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed during rest period")
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC pressed during rest period")
                    return None
        
        elapsed = clock.get_time() - start_time
        progress = elapsed / rest_duration  # 0.0 to 1.0
        
        # Interpolate from GREEN to YELLOW
        r = int(GREEN[0] + (YELLOW[0] - GREEN[0]) * progress)
        g = int(GREEN[1] + (YELLOW[1] - GREEN[1]) * progress)
        b = int(GREEN[2] + (YELLOW[2] - GREEN[2]) * progress)
        current_color = (r, g, b)
        
        screen.fill(current_color)
        pygame.display.flip()
    
    print("Rest period complete")
    
    # ========== PLAY ALARM SOUND ==========
    print("Playing alarm sound...")
    
    # Create a simple beep sound
    # This generates a 440 Hz tone for 0.5 seconds
    sample_rate = 22050
    duration = 0.5  # seconds
    frequency = 440  # Hz (A4 note)
    
    # Generate the sound
    import numpy as np
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
    print("Rest routine complete")
    print("=" * 50)
    
    return True