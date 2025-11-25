import pygame
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from glob import glob
from PIL import Image
import os

BERLIN_TZ = timezone(timedelta(hours=1))

def berlin_time_now():
    return datetime.now(BERLIN_TZ).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

class TimingTestConfig:
    """Configuration for timing test."""
    def __init__(self):
        self.time_mismatch = 0.0076  # Estimated time mismatch in seconds
        self.transition_time = 0.80 - self.time_mismatch  # 800ms transitions
        self.test_duration = 120.0  # 2 minutes in seconds
        self.target_fps = 60
        self.transition_steps = round(self.target_fps * self.transition_time)
        
        # Calculate number of images needed
        # Total transitions = test_duration / transition_time
        self.n_transitions = int(self.test_duration / self.transition_time)
        self.n_images = self.n_transitions + 1  # +1 for the initial image
        
        # Stimulus paths
        self.city_path = 'stimuli/scenes/city/*.png'
        self.mountain_path = 'stimuli/scenes/mountain/*.png'
        
        # Data output
        self.data_dir = 'data/gradcpt_timing_test'
        
        print(f"\nTiming Test Configuration:")
        print(f"  Duration: {self.test_duration}s ({self.test_duration/60:.1f} minutes)")
        print(f"  Transition time: {self.transition_time * 1000}ms")
        print(f"  Target FPS: {self.target_fps}")
        print(f"  Transition steps: {self.transition_steps}")
        print(f"  Expected transitions: {self.n_transitions}")
        print(f"  Expected images: {self.n_images}")

def load_and_process_image(filepath):
    """Load and process a single image."""
    img = Image.open(filepath).convert('L').resize((256, 256), Image.LANCZOS)
    img_array = np.array(img, dtype=np.float32)
    
    # Apply circular mask
    height, width = img_array.shape
    center_y, center_x = height / 2, width / 2
    radius = min(center_x, center_y)
    y, x = np.ogrid[:height, :width]
    mask = ((y - center_y) ** 2 + (x - center_x) ** 2) <= radius ** 2
    img_array[~mask] = 127.5
    
    # Normalize to [-1, 1]
    img_array = (img_array / 255.0) * 2.0 - 1.0
    return img_array

def gradcpt_timing_test(screen, clock, participant_id="test"):
    """
    Run timing test for gradCPT with precise measurements.
    """
    config = TimingTestConfig()
    
    # Load images
    print("\nLoading images...")
    city_files = glob(config.city_path)
    mountain_files = glob(config.mountain_path)
    
    if not city_files or not mountain_files:
        print("ERROR: Could not find stimulus images!")
        return None
    
    print(f"Found {len(city_files)} city images and {len(mountain_files)} mountain images")
    
    city_images = [load_and_process_image(f) for f in city_files]
    mountain_images = [load_and_process_image(f) for f in mountain_files]
    
    print(f"Loaded {len(city_images)} city and {len(mountain_images)} mountain images")
    
    # Generate random sequence (no consecutive duplicates)
    all_images = city_images + mountain_images
    sequence = []
    prev_img_idx = None
    
    for i in range(config.n_images):
        new_img_idx = prev_img_idx
        while new_img_idx == prev_img_idx:
            new_img_idx = np.random.randint(0, len(all_images))
        sequence.append(all_images[new_img_idx])
        prev_img_idx = new_img_idx
    
    print(f"Generated sequence of {len(sequence)} images")
    
    # Data structures
    image_times = []  # When each image reaches full visibility
    transition_durations = []  # Actual duration of each transition
    keypress_times = []  # When keys are pressed
    
    # Fonts
    font = pygame.font.Font(None, 36)
    
    # Instructions
    print("\n" + "="*50)
    print("TIMING TEST - INSTRUCTIONS")
    print("="*50)
    
    instructions = [
        "GradCPT Timing Test",
        "",
        f"Duration: {config.test_duration}s ({config.test_duration/60:.1f} minutes)",
        f"Expected transitions: {config.n_transitions}",
        f"Transition time: {config.transition_time * 1000}ms",
        "",
        "Press any key to respond (timing will be recorded)",
        "",
        "Press SPACE to begin"
    ]
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_SPACE:
                    waiting = False
        
        screen.fill((128, 128, 128))
        y_offset = 150
        for i, line in enumerate(instructions):
            text = font.render(line, True, (255, 255, 255))
            rect = text.get_rect(center=(400, y_offset + i * 40))
            screen.blit(text, rect)
        pygame.display.flip()
    
    # Start timing test
    print("\n" + "="*50)
    print("STARTING TIMING TEST")
    print("="*50)
    
    test_start_exp_time = clock.get_time()
    test_start_berlin_time = berlin_time_now()
    
    print(f"Start - Experiment time: {test_start_exp_time:.6f}s")
    print(f"Start - Berlin time: {test_start_berlin_time}")
    
    # Initialize
    current_img_idx = 0
    next_img_idx = 1
    last_image_completion_time = test_start_exp_time
    transition_start_time = test_start_exp_time
    
    # Generate initial transition (from gray to first image)
    gray = np.zeros((256, 256), dtype=np.float32)
    current_transition = np.linspace(gray, sequence[0], config.transition_steps, endpoint=False)
    
    # Prepare next transition
    if next_img_idx < len(sequence):
        next_transition = np.linspace(sequence[current_img_idx], sequence[next_img_idx], 
                                     config.transition_steps, endpoint=False)
    
    running = True
    pygame_clock = pygame.time.Clock()
    
    while running:
        current_time = clock.get_time()
        
        # Check if test duration exceeded
        if current_time - test_start_exp_time >= config.test_duration:
            print("\nTest duration reached - stopping")
            running = False
            break
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                
                # Log any keypress
                key_exp_time = clock.get_time()
                key_berlin_time = berlin_time_now()
                key_name = pygame.key.name(event.key)
                
                elapsed_in_transition = key_exp_time - transition_start_time
                transition_progress = elapsed_in_transition / config.transition_time
                
                keypress_times.append({
                    'experiment_time': key_exp_time,
                    'berlin_time': key_berlin_time,
                    'time_in_test': key_exp_time - test_start_exp_time,
                    'key': key_name,
                    'current_image_idx': current_img_idx,
                    'transition_progress': min(transition_progress, 1.0)
                })
                
                print(f"  Key pressed: {key_name} at {key_exp_time:.6f}s")
        
        # TIME-BASED TRANSITION
        # Calculate progress based on elapsed time
        elapsed_in_transition = current_time - transition_start_time
        transition_progress = elapsed_in_transition / config.transition_time  # 0.0 to 1.0
        
        # Clamp to valid range
        transition_progress = min(transition_progress, 1.0)
        
        # Get the appropriate frame from transition
        frame_idx = int(transition_progress * (config.transition_steps - 1))
        frame_idx = min(frame_idx, config.transition_steps - 1)
        
        img_array = current_transition[frame_idx]
        
        # Check if transition completed
        if transition_progress >= 1.0:
            # Image fully visible - log timing
            completion_time = current_time
            completion_berlin = berlin_time_now()
            
            # Calculate actual transition duration
            if current_img_idx > 0:  # Skip first gray->image transition
                actual_duration = (completion_time - last_image_completion_time) * 1000
                transition_durations.append({
                    'transition_idx': current_img_idx - 1,
                    'from_image': current_img_idx - 1,
                    'to_image': current_img_idx,
                    'expected_duration_ms': config.transition_time * 1000,
                    'actual_duration_ms': actual_duration,
                    'error_ms': actual_duration - (config.transition_time * 1000)
                })
                
                print(f"  Transition {current_img_idx-1}: {actual_duration:.2f}ms "
                      f"(error: {actual_duration - 800:.2f}ms)")
            
            # Log image appearance
            image_times.append({
                'image_idx': current_img_idx,
                'experiment_time': completion_time,
                'berlin_time': completion_berlin,
                'time_in_test': completion_time - test_start_exp_time
            })
            
            # Move to next image
            current_img_idx = next_img_idx
            next_img_idx += 1
            last_image_completion_time = completion_time
            transition_start_time = completion_time  # Reset transition timer
            
            # Update transitions
            if next_img_idx < len(sequence):
                current_transition = next_transition
                if next_img_idx < len(sequence):
                    next_transition = np.linspace(sequence[current_img_idx], sequence[next_img_idx],
                                                 config.transition_steps, endpoint=False)
            else:
                print(f"\nCompleted all {len(sequence)} images")
                running = False
                break
        
        # Render current frame
        img_display = ((img_array + 1) * 127.5).astype(np.uint8)
        img_rgb = np.stack([img_display, img_display, img_display], axis=-1)
        surf = pygame.surfarray.make_surface(np.transpose(img_rgb, (1, 0, 2)))
        surf = pygame.transform.scale(surf, (512, 512))
        
        screen.fill((128, 128, 128))
        screen.blit(surf, ((800 - 512) // 2, (600 - 512) // 2))
        pygame.display.flip()
        
        pygame_clock.tick(config.target_fps)
    
    # Test ended
    test_end_exp_time = clock.get_time()
    test_end_berlin_time = berlin_time_now()
    
    print("\n" + "="*50)
    print("TIMING TEST COMPLETE")
    print("="*50)
    print(f"End - Experiment time: {test_end_exp_time:.6f}s")
    print(f"End - Berlin time: {test_end_berlin_time}")
    print(f"Total duration: {test_end_exp_time - test_start_exp_time:.6f}s")
    
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
        'n_images_shown': len(image_times),
        'expected_images': config.n_images,
        'n_transitions': len(transition_durations),
        'expected_transitions': config.n_transitions,
        'n_keypresses': len(keypress_times),
        'target_fps': config.target_fps,
        'transition_time_ms': config.transition_time * 1000
    }
    
    summary_df = pd.DataFrame([summary_data])
    summary_df.to_csv(f"{config.data_dir}/timing_test_summary_{timestamp}.csv", index=False)
    
    # Image timing data
    if image_times:
        images_df = pd.DataFrame(image_times)
        images_df.to_csv(f"{config.data_dir}/timing_test_images_{timestamp}.csv", index=False)
        print(f"Saved {len(image_times)} image timing records")
    
    # Transition duration data
    if transition_durations:
        transitions_df = pd.DataFrame(transition_durations)
        transitions_df.to_csv(f"{config.data_dir}/timing_test_transitions_{timestamp}.csv", index=False)
        print(f"Saved {len(transition_durations)} transition duration records")
        
        # Print statistics
        mean_duration = transitions_df['actual_duration_ms'].mean()
        std_duration = transitions_df['actual_duration_ms'].std()
        mean_error = transitions_df['error_ms'].mean()
        max_error = transitions_df['error_ms'].abs().max()
        
        print(f"\nTransition Duration Statistics:")
        print(f"  Mean duration: {mean_duration:.2f}ms (expected: 800ms)")
        print(f"  Std deviation: {std_duration:.2f}ms")
        print(f"  Mean error: {mean_error:.2f}ms")
        print(f"  Max absolute error: {max_error:.2f}ms")
    
    # Keypress data
    if keypress_times:
        keypresses_df = pd.DataFrame(keypress_times)
        keypresses_df.to_csv(f"{config.data_dir}/timing_test_keypresses_{timestamp}.csv", index=False)
        print(f"Saved {len(keypress_times)} keypress records")
    
    print(f"\nAll data saved to: {config.data_dir}/")
    print("="*50)
    
    return True