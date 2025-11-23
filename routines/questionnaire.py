import pygame

def questionnaire_routine(screen, clock):
    """
    Display a questionnaire instruction screen.
    
    Args:
        screen: pygame display surface
        clock: Clock object for timing
    
    Returns:
        int: questionnaire number (1 or 2) to track which questionnaire to do next
        None: if routine was exited with ESC or window closed
    """
    # Track which questionnaire number we're on (static variable pattern)
    if not hasattr(questionnaire_routine, "counter"):
        questionnaire_routine.counter = 1
    
    current_number = questionnaire_routine.counter
    
    # Colors (matching your experiment style)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Font setup
    pygame.font.init()
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    
    # Main message
    main_text = f"Please open the tablet and do questionnaire #{current_number}."
    instruction_text = "Whenever you are ready, press SPACE to continue with the experiment"
    
    running = True
    space_pressed = False
    
    print(f"Questionnaire instruction screen displayed (#{current_number})")
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed during questionnaire instruction")
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC pressed during questionnaire instruction")
                    return None
                elif event.key == pygame.K_SPACE:
                    space_pressed = True
                    running = False
        
        # Clear screen
        screen.fill(BLACK)
        
        # Render text
        main_surface = font_large.render(main_text, True, WHITE)
        instruction_surface = font_medium.render(instruction_text, True, WHITE)
        
        # Center text on screen
        screen_width, screen_height = screen.get_size()
        main_rect = main_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        instruction_rect = instruction_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        
        # Blit text
        screen.blit(main_surface, main_rect)
        screen.blit(instruction_surface, instruction_rect)
        
        # Update display
        pygame.display.flip()
    
    if space_pressed:
        print(f"Questionnaire #{current_number} instruction acknowledged - continuing experiment")
        # Increment counter for next call
        questionnaire_routine.counter += 1
        return current_number
    
    return None


def reset_questionnaire_counter():
    """Reset the questionnaire counter back to 1."""
    questionnaire_routine.counter = 1