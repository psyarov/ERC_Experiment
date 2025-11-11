# core/gradcpt_config.py
import random

class GradCPTConfig:
    """Configuration class for GradCPT parameters."""
    
    def __init__(self):
        # Task parameters
        self.n_trials = 80  # Number of trials per block
        self.n_blocks = 2   # Number of blocks
        self.prop_dom = 0.9  # Proportion of dominant (city) stimuli
        
        # Timing parameters
        self.transition_time = 0.40  # Time in seconds for morphing
        self.target_fps = 60  # Target frame rate
        self.transition_steps = round(self.target_fps * self.transition_time)
        
        # Response mapping (randomly assigned)
        if random.choice([True, False]):
            self.dom_key = 'j'
            self.nondom_key = 'f'
        else:
            self.dom_key = 'f'
            self.nondom_key = 'j'
        
        # Stimulus paths
        #self.dom_stim_path = 'stimuli/scenes/city/*.jpg'
        self.dom_stim_path = 'stimuli/scenes/city/*png'
        #self.nondom_stim_path = 'stimuli/scenes/mountain/*.jpg'
        self.nondom_stim_path = 'stimuli/scenes/mountain/*.png'
        
        # Data output
        self.data_dir = 'data/gradcpt'
        self.participant_id = None  # Set this before running
        
        # Calculated parameters
        self.n_dom = round(self.n_trials * self.prop_dom)
        self.n_nondom = self.n_trials - self.n_dom
    
    def set_participant_id(self, pid):
        """Set the participant ID for data saving."""
        self.participant_id = pid
    
    def update_fps(self, measured_fps):
        """Update transition steps based on measured frame rate."""
        self.target_fps = measured_fps
        self.transition_steps = round(self.target_fps * self.transition_time)
        print(f"Updated FPS: {self.target_fps:.2f} Hz, Transition steps: {self.transition_steps}")
    
    def __str__(self):
        return (f"GradCPT Config:\n"
                f"  Trials per block: {self.n_trials}\n"
                f"  Blocks: {self.n_blocks}\n"
                f"  Dominant key: {self.dom_key}\n"
                f"  Non-dominant key: {self.nondom_key}\n"
                f"  Target FPS: {self.target_fps}\n"
                f"  Transition steps: {self.transition_steps}")