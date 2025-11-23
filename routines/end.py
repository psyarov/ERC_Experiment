import pygame

def end(screen, clock):
    """
    End routine displaying thank you message.
    
    Args:
        screen: pygame display surface
        clock: Clock object for timing
    
    Returns:
        True: when routine is acknowledged or exited
    """
    # Colors
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    
    # Font setup
    pygame.font.init()
    font_large = pygame.font.Font(None, 60)
    
    screen_width, screen_height = screen.get_size()
    
    # ========== END SCREEN ==========
    print("=" * 50)
    print("EXPERIMENT END")
    print("=" * 50)
    
    message_line1 = "This is the end of the experiment."
    message_line2 = "Thank you for participating."
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed")
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    waiting = False
        
        screen.fill(GRAY)
        
        # Render message text
        text1_surface = font_large.render(message_line1, True, WHITE)
        text1_rect = text1_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
        screen.blit(text1_surface, text1_rect)
        
        text2_surface = font_large.render(message_line2, True, WHITE)
        text2_rect = text2_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
        screen.blit(text2_surface, text2_rect)
        
        pygame.display.flip()
    
    print("Experiment ended - thank you message acknowledged")
    print("=" * 50)
    
    return True