import pygame

def short_break(screen, clock):
    """
    Break routine allowing participant to rest before continuing.
    
    Args:
        screen: pygame display surface
        clock: Clock object for timing
    
    Returns:
        True: if routine completed successfully (SPACE pressed)
        None: if routine was exited with ESC or window closed
    """
    # Colors
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    
    # Font setup
    pygame.font.init()
    font_large = pygame.font.Font(None, 48)
    
    screen_width, screen_height = screen.get_size()
    
    # ========== BREAK SCREEN ==========
    print("=" * 50)
    print("BREAK ROUTINE")
    print("=" * 50)
    print("Participant taking a break...")
    
    message_line1 = "You can have a short break."
    message_line2 = "Press SPACE whenever you are ready to continue."
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed during break")
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC pressed during break")
                    return None
                elif event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_4:
                    print("Skipping short break (pressed 4)")
                    return True
        
        screen.fill(GRAY)
        
        # Render message text
        text1_surface = font_large.render(message_line1, True, WHITE)
        text1_rect = text1_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        screen.blit(text1_surface, text1_rect)
        
        text2_surface = font_large.render(message_line2, True, WHITE)
        text2_rect = text2_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
        screen.blit(text2_surface, text2_rect)
        
        pygame.display.flip()
    
    print("Break complete - participant ready to continue")
    print("=" * 50)
    
    return True