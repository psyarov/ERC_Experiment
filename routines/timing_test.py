import pygame
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from PIL import Image
import os

BERLIN_TZ = timezone(timedelta(hours=1))

def berlin_time_now():
    return datetime.now(BERLIN_TZ).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

class BoxTimingConfig:
    """Configuration for box alternation timing test."""
    def __init__(self):
        self.transition_time = 0.800  # 800ms per state
        self.test_duration = 60.0  # 1 minute in seconds
        
        # Calculate number of transitions
        self.n_transitions = int(self.test_duration / self.transition_time)
        
        # Image paths
        self.white_image_path = '/Users/pavelsyarov/Desktop/CHARITE/Rotations/IBS/ERC/official_xp_code/ERC_Experiment/stimuli/colors/white.png'
        self.black_image_path = '/Users/pavelsyarov/Desktop/CHARITE/Rotations/IBS/ERC/official_xp_code/ERC_Experiment/stimuli/colors/black.png'
        
        # Data output
        self.data_dir = 'data/box_timing_test'
        
        print(f"\nBox Timing Test Configuration:")
        print(f"  Duration: {self.test_duration}s")
        print(f"  Transition time: {self.transition_time * 1000}ms")
        print(f"  Expected transitions: {self.n_transitions}")

def load_box_image(filepath):
    """Load and process a box image."""
    try:
        img = Image.open(filepath).convert('RGB')
        img_array = np.array(img, dtype=np.uint8)
        return img_array
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}")
        # Create default images if files don't exist
        if 'white' in filepath:
            return np.ones((100, 100, 3), dtype=np.uint8) * 255
        else:
            return np.zeros((100, 100, 3), dtype=np.uint8)

def box_alternation_test(participant_id="test"):
    """
    Run box alternation timing test with precise measurements.
    """
    # Initialize pygame
    pygame.init()
    
    # Get display info for fullscreen
    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    
    # Create fullscreen window
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Box Timing Test")
    
    # Create custom clock
    clock = pygame.time.Clock()
    
    # Timer class to track experiment time
    class ExperimentClock:
        def __init__(self):
            self.start_ticks = pygame.time.get_ticks()
        
        def get_time(self):
            return (pygame.time.get_ticks() - self.start_ticks) / 1000.0
    
    exp_clock = ExperimentClock()
    
    config = BoxTimingConfig()
    
    # Load images
    print("\nLoading box images...")
    white_img = load_box_image(config.white_image_path)
    black_img = load_box_image(config.black_image_path)
    
    print(f"White image shape: {white_img.shape}")
    print(f"Black image shape: {black_img.shape}")
    
    # Convert to pygame surfaces
    white_surf = pygame.surfarray.make_surface(np.transpose(white_img, (1, 0, 2)))
    black_surf = pygame.surfarray.make_surface(np.transpose(black_img, (1, 0, 2)))
    
    box_size = white_surf.get_size()
    print(f"Box size: {box_size}")
    
    # Data structures
    transition_times = []  # When each transition occurs
    state_durations = []  # How long each state lasted
    keypress_times = []  # When keys are pressed
    
    # Fonts
    font = pygame.font.Font(None, 48)
    
    # Instructions screen
    print("\n" + "="*50)
    print("BOX TIMING TEST - INSTRUCTIONS")
    print("="*50)
    
    instructions = [
        "Box Alternation Timing Test",
        "",
        f"Duration: {config.test_duration}s (1 minute)",
        f"Box alternation time: {config.transition_time * 1000}ms",
        "",
        "A box in the top-left corner will alternate",
        "between white and black every 800ms.",
        "",
        "Press SPACE to begin",
        "Press ESC to quit"
    ]
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None
                elif event.key == pygame.K_SPACE:
                    waiting = False
        
        screen.fill((128, 128, 128))  # Gray background
        y_offset = screen_height // 2 - 200
        for i, line in enumerate(instructions):
            text = font.render(line, True, (255, 255, 255))
            rect = text.get_rect(center=(screen_width // 2, y_offset + i * 50))
            screen.blit(text, rect)
        pygame.display.flip()
    
    # Start timing test
    print("\n" + "="*50)
    print("STARTING BOX TIMING TEST")
    print("="*50)
    
    # Reset clock for test
    exp_clock = ExperimentClock()
    test_start_exp_time = exp_clock.get_time()
    test_start_berlin_time = berlin_time_now()
    
    print(f"Start - Experiment time: {test_start_exp_time:.6f}s")
    print(f"Start - Berlin time: {test_start_berlin_time}")
    
    # Initialize state
    current_state = 'white'  # Start with white
    state_start_time = test_start_exp_time
    transition_count = 0
    
    # Log initial state
    transition_times.append({
        'transition_idx': 0,
        'state': current_state,
        'experiment_time': test_start_exp_time,
        'berlin_time': test_start_berlin_time,
        'time_in_test': 0.0
    })
    
    running = True
    
    while running:
        current_time = exp_clock.get_time()
        elapsed_in_test = current_time - test_start_exp_time
        
        # Check if test duration exceeded
        if elapsed_in_test >= config.test_duration:
            print("\nTest duration reached - stopping")
            
            # Log final state duration
            final_duration = (current_time - state_start_time) * 1000
            state_durations.append({
                'state_idx': transition_count,
                'state': current_state,
                'expected_duration_ms': config.transition_time * 1000,
                'actual_duration_ms': final_duration,
                'error_ms': final_duration - (config.transition_time * 1000)
            })
            
            running = False
            break
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                
                # Log any keypress
                key_exp_time = exp_clock.get_time()
                key_berlin_time = berlin_time_now()
                key_name = pygame.key.name(event.key)
                
                keypress_times.append({
                    'experiment_time': key_exp_time,
                    'berlin_time': key_berlin_time,
                    'time_in_test': key_exp_time - test_start_exp_time,
                    'key': key_name,
                    'current_state': current_state,
                    'transition_count': transition_count
                })
                
                print(f"  Key pressed: {key_name} at {key_exp_time:.6f}s (state: {current_state})")
        
        if not running:
            break
        
        # Check if it's time to transition
        time_in_state = current_time - state_start_time
        
        if time_in_state >= config.transition_time:
            # Calculate actual duration of previous state
            actual_duration = time_in_state * 1000  # Convert to ms
            
            state_durations.append({
                'state_idx': transition_count,
                'state': current_state,
                'expected_duration_ms': config.transition_time * 1000,
                'actual_duration_ms': actual_duration,
                'error_ms': actual_duration - (config.transition_time * 1000)
            })
            
            print(f"  State {transition_count} ({current_state}): {actual_duration:.2f}ms "
                  f"(error: {actual_duration - 800:.2f}ms)")
            
            # Transition to next state
            current_state = 'black' if current_state == 'white' else 'white'
            state_start_time = current_time
            transition_count += 1
            
            # Log transition
            transition_berlin_time = berlin_time_now()
            transition_times.append({
                'transition_idx': transition_count,
                'state': current_state,
                'experiment_time': current_time,
                'berlin_time': transition_berlin_time,
                'time_in_test': elapsed_in_test
            })
        
        # Render current state
        screen.fill((128, 128, 128))  # Gray background
        
        # Draw box in top-left corner
        if current_state == 'white':
            screen.blit(white_surf, (0, 0))
        else:
            screen.blit(black_surf, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    # Test ended
    test_end_exp_time = exp_clock.get_time()
    test_end_berlin_time = berlin_time_now()
    
    print("\n" + "="*50)
    print("BOX TIMING TEST COMPLETE")
    print("="*50)
    print(f"End - Experiment time: {test_end_exp_time:.6f}s")
    print(f"End - Berlin time: {test_end_berlin_time}")
    print(f"Total duration: {test_end_exp_time - test_start_exp_time:.6f}s")
    print(f"Total transitions: {transition_count}")
    
    # Save data
    print("\nSaving timing data...")
    os.makedirs(config.data_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Summary data
    summary_data = {
        'participant_id': participant_id,
        'test_start_exp_time': test_start_exp_time,
        'test_start_berlin_time': test_start_berlin_time,
        'test_end_exp_time': test_end_exp_time,
        'test_end_berlin_time': test_end_berlin_time,
        'actual_duration_s': test_end_exp_time - test_start_exp_time,
        'expected_duration_s': config.test_duration,
        'n_transitions': transition_count,
        'expected_transitions': config.n_transitions,
        'n_keypresses': len(keypress_times),
        'transition_time_ms': config.transition_time * 1000
    }
    
    summary_df = pd.DataFrame([summary_data])
    summary_df.to_csv(f"{config.data_dir}/box_timing_summary_{timestamp}.csv", index=False)
    
    # Transition timing data
    if transition_times:
        transitions_df = pd.DataFrame(transition_times)
        transitions_df.to_csv(f"{config.data_dir}/box_transitions_{timestamp}.csv", index=False)
        print(f"Saved {len(transition_times)} transition timing records")
    
    # State duration data
    if state_durations:
        durations_df = pd.DataFrame(state_durations)
        durations_df.to_csv(f"{config.data_dir}/box_state_durations_{timestamp}.csv", index=False)
        print(f"Saved {len(state_durations)} state duration records")
        
        # Print statistics
        mean_duration = durations_df['actual_duration_ms'].mean()
        std_duration = durations_df['actual_duration_ms'].std()
        mean_error = durations_df['error_ms'].mean()
        max_error = durations_df['error_ms'].abs().max()
        
        print(f"\nState Duration Statistics:")
        print(f"  Mean duration: {mean_duration:.2f}ms (expected: 800ms)")
        print(f"  Std deviation: {std_duration:.2f}ms")
        print(f"  Mean error: {mean_error:.2f}ms")
        print(f"  Max absolute error: {max_error:.2f}ms")
    
    # Keypress data
    if keypress_times:
        keypresses_df = pd.DataFrame(keypress_times)
        keypresses_df.to_csv(f"{config.data_dir}/box_keypresses_{timestamp}.csv", index=False)
        print(f"Saved {len(keypress_times)} keypress records")
    
    print(f"\nAll data saved to: {config.data_dir}/")
    print("="*50)
    
    # Close pygame
    pygame.quit()
    
    return True

if __name__ == "__main__":
    # Run the test
    result = box_alternation_test(participant_id="P001")
    
    if result:
        print("\nTest completed successfully!")
    else:
        print("\nTest was cancelled.")