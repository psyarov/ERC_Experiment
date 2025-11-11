# core/gradcpt_data.py
import os
import pandas as pd
from datetime import datetime

class DataLogger:
    """Handles data logging for GradCPT."""
    
    def __init__(self, config, clock):
        self.config = config
        self.clock = clock
        self.experiment_start_time = datetime.now()
        self.data = []
        
        # Frame counter (global across all blocks)
        self.frame_count = 0
    
    def log_response(self, block, trial, condition, key_pressed, rt, transition_step, coherence):
        """Log a key press response."""
        self.frame_count += 1
        
        entry = {
            'subject': self.config.participant_id or 'unknown',
            'block': block + 1,  # 1-indexed for output
            'trial': trial + 1,  # 1-indexed for output
            'condition': condition,
            'stimulus_type': 'city' if condition == 'dom' else 'mountain',
            'correct_key': self.config.dom_key if condition == 'dom' else self.config.nondom_key,
            'key_pressed': key_pressed,
            'rt': rt,
            'transition_step': transition_step,
            'coherence': coherence,
            'frame_count': self.frame_count,
            'experiment_time': self.clock.get_time(),
            'wall_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            'response_type': 'response'
        }
        
        # Determine correctness
        if condition == 'dom':
            entry['correct'] = 1 if key_pressed == self.config.dom_key else 0
        else:
            entry['correct'] = 1 if key_pressed == self.config.nondom_key else 0
        
        self.data.append(entry)
        
        print(f"    Response: Trial {trial+1}, Key={key_pressed}, RT={rt:.3f}s, Coherence={coherence:.2f}")
    
    def log_omission(self, block, trial, condition):
        """Log an omission (no response)."""
        self.frame_count += 1
        
        entry = {
            'subject': self.config.participant_id or 'unknown',
            'block': block + 1,
            'trial': trial + 1,
            'condition': condition,
            'stimulus_type': 'city' if condition == 'dom' else 'mountain',
            'correct_key': self.config.dom_key if condition == 'dom' else self.config.nondom_key,
            'key_pressed': None,
            'rt': 0,
            'transition_step': self.config.transition_steps,
            'coherence': 1.0,
            'frame_count': self.frame_count,
            'experiment_time': self.clock.get_time(),
            'wall_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            'response_type': 'omission'
        }
        
        # Omissions on non-dominant trials are technically correct
        if condition == 'nondom':
            entry['correct'] = 1
        else:
            entry['correct'] = 0
        
        self.data.append(entry)
        
        print(f"    Omission: Trial {trial+1} ({condition})")
    
    def save_all_data(self):
        """Save all collected data to CSV."""
        if not self.data:
            print("No data to save!")
            return
        
        # Create data directory if it doesn't exist
        os.makedirs(self.config.data_dir, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        subject_id = self.config.participant_id or 'unknown'
        filename = f"{self.config.data_dir}/sub-{subject_id}_task-gradcpt_{timestamp}.csv"
        
        # Convert to DataFrame and save
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        
        print(f"Data saved to: {filename}")
        
        # Print summary statistics
        self._print_summary(df)
    
    def _print_summary(self, df):
        """Print summary statistics."""
        total_trials = len(df)
        responses = df[df['response_type'] == 'response']
        omissions = df[df['response_type'] == 'omission']
        
        print("\n=== GradCPT Summary ===")
        print(f"Total trials: {total_trials}")
        print(f"Responses: {len(responses)}")
        print(f"Omissions: {len(omissions)}")
        
        if len(responses) > 0:
            mean_rt = responses['rt'].mean()
            print(f"Mean RT: {mean_rt:.3f}s")
            
            correct = df[df['correct'] == 1]
            accuracy = len(correct) / total_trials * 100
            print(f"Accuracy: {accuracy:.1f}%")
            
            # Commission errors (false alarms on non-dominant)
            commissions = df[(df['condition'] == 'nondom') & (df['key_pressed'].notna())]
            if len(commissions) > 0:
                commission_rate = len(commissions) / len(df[df['condition'] == 'nondom']) * 100
                print(f"Commission error rate: {commission_rate:.1f}%")
            
            # Omission errors (misses on dominant)
            omission_errors = df[(df['condition'] == 'dom') & (df['key_pressed'].isna())]
            if len(omission_errors) > 0:
                omission_rate = len(omission_errors) / len(df[df['condition'] == 'dom']) * 100
                print(f"Omission error rate: {omission_rate:.1f}%")
        
        print("=======================\n")