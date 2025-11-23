import pygame

def breathing_calibration(screen, clock):
    """
    Breathing calibration routine with breath-holding cycles and break.
    
    Args:
        screen: pygame display surface
        clock: Clock object for timing
    
    Returns:
        True: if routine completed successfully
        None: if routine was exited with ESC or window closed
    """
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    GREEN = (0, 150, 0)
    RED = (150, 0, 0)
    YELLOW = (200, 200, 0)
    
    # Font setup
    pygame.font.init()
    font_large = pygame.font.Font(None, 60)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)
    
    screen_width, screen_height = screen.get_size()
    
    # ========== INTRO SCREEN ==========
    print("=" * 50)
    print("BREATHING CALIBRATION - INTRO")
    print("=" * 50)
    
    intro_lines = [
        "You will shortly be asked to either hold your breath",
        "or relax and breathe normally.",
        "Please follow the instructions on the screen.",
        "",
        "Press SPACE to continue."
    ]
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed during breathing calibration intro")
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC pressed during breathing calibration intro")
                    return None
                elif event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_4:
                    print("Skipping breathing calibration (pressed 4)")
                    return True
        
        screen.fill(GRAY)
        
        # Render intro text
        y_offset = screen_height // 2 - 100
        for line in intro_lines:
            text_surface = font_small.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 50
        
        pygame.display.flip()
    
    print("Intro acknowledged - starting breathing calibration")
    
    # ========== INITIAL NORMAL BREATHING (10s) ==========
    print("\nInitial normal breathing (10s)...")
    start_time = clock.get_time()
    duration = 10.0
    
    while clock.get_time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_4:
                    print("Skipping breathing calibration (pressed 4)")
                    return True
        
        elapsed = clock.get_time() - start_time
        remaining = duration - elapsed
        
        screen.fill(GREEN)
        
        # Instructions
        instruction_surface = font_large.render("Breathe normally", True, WHITE)
        instruction_rect = instruction_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(instruction_surface, instruction_rect)
        
        # Countdown
        countdown_text = f"{remaining:.1f}s"
        countdown_surface = font_medium.render(countdown_text, True, WHITE)
        countdown_rect = countdown_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(countdown_surface, countdown_rect)
        
        pygame.display.flip()
    
    print("Initial breathing complete")
    
    # ========== BREATH-HOLDING CYCLES (5 cycles) ==========
    print("\nStarting 5 breath-holding cycles...")
    num_cycles = 5
    hold_duration = 15.0
    recovery_duration = 35.0
    
    for cycle in range(1, num_cycles + 1):
        print(f"\nCycle {cycle}/{num_cycles}")
        
        # BREATH-HOLDING PHASE (15s, RED)
        print(f"  Breath-holding (15s)...")
        start_time = clock.get_time()
        
        while clock.get_time() - start_time < hold_duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_4:
                        print("Skipping breathing calibration (pressed 4)")
                        return True
            
            elapsed = clock.get_time() - start_time
            remaining = hold_duration - elapsed
            
            screen.fill(RED)
            
            # Instructions
            instruction_surface = font_large.render("Hold your breath!", True, WHITE)
            instruction_rect = instruction_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            screen.blit(instruction_surface, instruction_rect)
            
            # Timer
            timer_text = f"Time remaining: {remaining:.1f}s"
            timer_surface = font_medium.render(timer_text, True, WHITE)
            timer_rect = timer_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            screen.blit(timer_surface, timer_rect)
            
            pygame.display.flip()
        
        print(f"  Breath-holding complete")
        
        # RECOVERY PHASE (35s, GREEN)
        print(f"  Recovery (35s)...")
        start_time = clock.get_time()
        
        while clock.get_time() - start_time < recovery_duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_4:
                        print("Skipping breathing calibration (pressed 4)")
                        return True
            
            elapsed = clock.get_time() - start_time
            remaining = recovery_duration - elapsed
            
            screen.fill(GREEN)
            
            # Instructions
            instruction_surface = font_large.render("Breathe normally", True, WHITE)
            instruction_rect = instruction_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            screen.blit(instruction_surface, instruction_rect)
            
            # Timer
            timer_text = f"Time remaining: {remaining:.1f}s"
            timer_surface = font_medium.render(timer_text, True, WHITE)
            timer_rect = timer_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            screen.blit(timer_surface, timer_rect)
            
            pygame.display.flip()
        
        print(f"  Recovery complete")
    
    print("\nAll 5 cycles complete")
    
    # Reset to gray background
    screen.fill(GRAY)
    pygame.display.flip()
    
    # ========== BREAK SCREEN (120s with gradual yellow) ==========
    print("\nStarting 2-minute break with gradual yellow transition...")
    
    break_lines = [
        "Before we continue with the next part of the experiment,",
        "we will have a short break.",
        "",
        "In the next two minutes, just relax.",
        "The screen will gradually turn yellow as the time runs out.",
        "You do not need to press anything."
    ]
    
    start_time = clock.get_time()
    break_duration = 120.0
    
    while clock.get_time() - start_time < break_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_4:
                    print("Skipping breathing calibration (pressed 4)")
                    return True
        
        elapsed = clock.get_time() - start_time
        progress = elapsed / break_duration  # 0.0 to 1.0
        
        # Interpolate from GRAY to YELLOW
        r = int(GRAY[0] + (YELLOW[0] - GRAY[0]) * progress)
        g = int(GRAY[1] + (YELLOW[1] - GRAY[1]) * progress)
        b = int(GRAY[2] + (YELLOW[2] - GRAY[2]) * progress)
        current_color = (r, g, b)
        
        screen.fill(current_color)
        
        # Render break text
        y_offset = screen_height // 2 - 120
        for line in break_lines:
            text_surface = font_small.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 45
        
        pygame.display.flip()
    
    print("Break complete - breathing calibration finished")
    print("=" * 50)
    
    # Reset to gray background
    screen.fill(GRAY)
    pygame.display.flip()
    
    return True