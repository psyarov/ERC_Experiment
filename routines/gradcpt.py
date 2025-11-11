# routines/gradcpt.py
import pygame
import numpy as np
from datetime import datetime
from core.gradcpt_config import GradCPTConfig
from core.gradcpt_stimulus import StimulusManager
from core.gradcpt_data import DataLogger

def gradCPT_routine(screen, clock, config=None):
    """
    Run the gradCPT routine.
    
    Args:
        screen: pygame surface to draw on
        clock: Clock object for timing
        config: GradCPTConfig object (optional, will use defaults if None)
    
    Returns:
        True if completed successfully
        False if failed
        None if ESC or window closed
    """
    # Initialize configuration
    if config is None:
        config = GradCPTConfig()
    
    # Initialize components
    stim_manager = StimulusManager(config)
    data_logger = DataLogger(config, clock)
    
    # Fonts
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    
    # Instructions screen
    if not show_instructions(screen, clock, config, font_medium, font_small):
        return None
    
    # Run all blocks
    for block_num in range(config.n_blocks):
        print(f"\n=== Starting Block {block_num + 1}/{config.n_blocks} ===")
        
        # Block start screen
        if not show_block_start(screen, clock, config, font_medium, block_num):
            return None
        
        # Run the block
        result = run_gradcpt_block(screen, clock, config, stim_manager, data_logger, block_num)
        
        if result is None:
            return None
        elif not result:
            return False
        
        # Block rest screen (except after last block)
        if block_num < config.n_blocks - 1:
            if not show_block_rest(screen, clock, font_medium):
                return None
    
    # Save final data
    print("\n=== Saving data ===")
    data_logger.save_all_data()
    print("Data saved successfully!")
    
    return True


def show_instructions(screen, clock, config, font_medium, font_small):
    """Show instruction screen."""
    instructions = [
        "GradCPT Instructions",
        "",
        f"Press '{config.dom_key.upper()}' when you see a CITY scene",
        f"Press '{config.nondom_key.upper()}' when you see a MOUNTAIN scene",
        "",
        "Images will gradually morph into each other.",
        "Respond as quickly and accurately as possible.",
        "",
        "Press SPACE to continue"
    ]
    
    running = True
    pygame_clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_SPACE:
                    return True
        
        screen.fill((128, 128, 128))  # Gray background
        
        y_offset = 150
        for i, line in enumerate(instructions):
            if i == 0:
                text = font_medium.render(line, True, (255, 255, 255))
            else:
                text = font_small.render(line, True, (255, 255, 255))
            rect = text.get_rect(center=(400, y_offset + i * 35))
            screen.blit(text, rect)
        
        pygame.display.flip()
        pygame_clock.tick(60)
    
    return None


def show_block_start(screen, clock, config, font_medium, block_num):
    """Show block start screen."""
    lines = [
        f"Block {block_num + 1} of {config.n_blocks}",
        "",
        f"Press '{config.dom_key.upper()}' for CITY",
        f"Press '{config.nondom_key.upper()}' for MOUNTAIN",
        "",
        "Press SPACE to begin"
    ]
    
    running = True
    pygame_clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_SPACE:
                    return True
        
        screen.fill((128, 128, 128))
        
        y_offset = 200
        for i, line in enumerate(lines):
            text = font_medium.render(line, True, (255, 255, 255))
            rect = text.get_rect(center=(400, y_offset + i * 40))
            screen.blit(text, rect)
        
        pygame.display.flip()
        pygame_clock.tick(60)
    
    return None


def show_block_rest(screen, clock, font_medium):
    """Show rest screen between blocks."""
    text = "Take a short break. Press SPACE to continue."
    
    running = True
    pygame_clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_SPACE:
                    return True
        
        screen.fill((128, 128, 128))
        rendered = font_medium.render(text, True, (255, 255, 255))
        rect = rendered.get_rect(center=(400, 300))
        screen.blit(rendered, rect)
        
        pygame.display.flip()
        pygame_clock.tick(60)
    
    return None


def run_gradcpt_block(screen, clock, config, stim_manager, data_logger, block_num):
    """
    Run a single block of gradCPT trials.
    """
    # Generate stimulus sequence for this block
    stim_manager.generate_sequence()
    
    # Initialize block
    trial_idx = 0
    transition_step = 0
    pressed_key_this_trial = False
    trial_start_time = clock.get_time()
    block_start_time = clock.get_time()
    
    # Get initial transitions
    current_transition = stim_manager.get_initial_transition()
    next_transition = stim_manager.get_transition(0, 1)
    
    running = True
    pygame_clock = pygame.time.Clock()
    
    print(f"Starting block with {config.n_trials} trials...")
    
    while running and trial_idx < config.n_trials:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                
                # Check for valid response keys
                key_name = pygame.key.name(event.key)
                if key_name in [config.dom_key, config.nondom_key]:
                    if not pressed_key_this_trial:
                        rt = clock.get_time() - trial_start_time
                        coherence = transition_step / config.transition_steps
                        
                        data_logger.log_response(
                            block=block_num,
                            trial=trial_idx,
                            condition=stim_manager.conditions[trial_idx],
                            key_pressed=key_name,
                            rt=rt,
                            transition_step=transition_step,
                            coherence=coherence
                        )
                        pressed_key_this_trial = True
        
        # Check if we've reached the end of transition
        if transition_step >= config.transition_steps:
            # Log omission if no key was pressed
            if not pressed_key_this_trial:
                data_logger.log_omission(
                    block=block_num,
                    trial=trial_idx,
                    condition=stim_manager.conditions[trial_idx]
                )
            
            # Move to next trial
            trial_idx += 1
            transition_step = 0
            pressed_key_this_trial = False
            trial_start_time = clock.get_time()
            
            # Update transitions
            if trial_idx < config.n_trials:
                current_transition = next_transition
                if trial_idx + 1 < config.n_trials:
                    next_transition = stim_manager.get_transition(trial_idx, trial_idx + 1)
                
                # Progress feedback
                if trial_idx % 10 == 0:
                    print(f"  Trial {trial_idx}/{config.n_trials} completed")
            else:
                # Block finished
                running = False
                break
        
        # Get current image from transition
        img_array = current_transition[transition_step]
        
        # Convert numpy array to pygame surface
        # img_array is (256, 256) normalized to [-1, 1], need to convert to [0, 255]
        img_display = ((img_array + 1) * 127.5).astype(np.uint8)
        
        # For grayscale, we need to create an RGB surface
        # Stack the grayscale array 3 times to make it RGB
        img_rgb = np.stack([img_display, img_display, img_display], axis=-1)

        # Create surface (pygame expects width x height x 3)
        surf = pygame.surfarray.make_surface(np.transpose(img_rgb, (1, 0, 2)))

        surf = pygame.transform.scale(surf, (512, 512))  # 2x scale
        
        # Draw
        screen.fill((128, 128, 128))
        screen.blit(surf, ((800 - 512) // 2, (600 - 512) // 2))
        
        pygame.display.flip()
        
        # Increment frame
        transition_step += 1
        pygame_clock.tick(config.target_fps)
    
    print(f"Block {block_num + 1} completed!")
    return True