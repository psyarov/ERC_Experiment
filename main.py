import os
import pygame
from core.clock import Clock
from core.fps_estimator import FPSEstimator
from core.gradcpt_config import GradCPTConfig
from datetime import datetime, timezone, timedelta

from routines.welcome import welcome_routine
from routines.gradcpt import gradCPT_routine
from routines.questionnaire import questionnaire_routine
from routines.breathing_calibration import breathing_calibration
from routines.rest import rest
from routines.videos import videos
from routines.short_break import short_break


# Init
print("Launching main.py...")
print("Initializing pygame...")
pygame.init()
print("Creating screen...")
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Experiment Window")
print("Setting up clock...")
clock = Clock()

BERLIN_TZ = timezone(timedelta(hours=1))

def berlin_time_now():
    return datetime.now(BERLIN_TZ).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

running = True
print("Experiment running!\n\nHELLO, WORLD!\n\n")

# Estimate frame rate
print("=" * 50)
print("FRAME RATE ESTIMATION")
print("=" * 50)
fps_estimator = FPSEstimator(duration=5.0)
measured_fps = fps_estimator.estimate(screen, clock)

if measured_fps is None:
    print("Frame rate estimation cancelled")
    running = False
else:
    print(f"Measured FPS: {measured_fps:.2f} Hz")
    print("=" * 50)

# Setup GradCPT configuration
if running:
    config = GradCPTConfig()
    config.update_fps(measured_fps)
    config.set_participant_id("001")  # You can make this dynamic
    print("\n" + str(config))
    print()

# Run welcome routine
if running:
    print("=" * 50)
    print("WELCOME ROUTINE")
    print("=" * 50)
    result = welcome_routine(screen, clock)
    if result is None:
        print("Welcome routine exited (ESC or window closed)")
        running = False
    elif result:
        print("Welcome routine: SUCCESS - continuing with experiment")
    else:
        print("Welcome routine: FAIL - continuing with experiment")
    print()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# RUN EXPERIMENT ROUTINES
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run TRAIT-LEVEL QUESTIONNAIRE
result = questionnaire_routine(screen, clock)

if result is None:
    print("Questionnaire routine exited")
    running = False
else:
    print(f"Completed questionnaire instruction #{result}")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run breathing calibration #1
result = breathing_calibration(screen, clock)

if result is None:
    print("Breathing calibration exited")
    running = False
else:
    print("Breathing calibration: SUCCESS")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run rest routine #1
result = rest(screen, clock)
if result is None:
    print("Rest routine exited")
    running = False
else:
    print("Rest routine: SUCCESS")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run STATE-LEVEL QUESTIONNAIRE #1 (before first S-TOL )
result = questionnaire_routine(screen, clock)

if result is None:
    print("Questionnaire routine exited")
    running = False
else:
    print(f"Completed questionnaire instruction #{result}")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run S-TOL #1
# (Placeholder for S-TOL routine, not implemented in this snippet)
print("S-TOL #1 routine would run here.")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run STATE-LEVEL QUESTIONNAIRE #2 (after first S-TOL )
result = questionnaire_routine(screen, clock)

if result is None:
    print("Questionnaire routine exited")
    running = False
else:
    print(f"Completed questionnaire instruction #{result}")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run break routine #1
result = short_break(screen, clock)
if result is None:
    print("Break routine exited")
    running = False
else:
    print("Break routine: SUCCESS")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run rest routine #2
result = rest(screen, clock)
if result is None:
    print("Rest routine exited")
    running = False
else:
    print("Rest routine: SUCCESS")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run STATE-LEVEL QUESTIONNAIRE #3 (before first gradCPT )
result = questionnaire_routine(screen, clock)

if result is None:
    print("Questionnaire routine exited")
    running = False
else:
    print(f"Completed questionnaire instruction #{result}")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run gradCPT #1
if running:
    result = gradCPT_routine(screen, clock, config)

    if result is None:
        print("GradCPT routine exited")
        running = False
    elif result:
        print("GradCPT routine: SUCCESS")
    else:
        print("GradCPT routine: FAIL")
    print()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run STATE-LEVEL QUESTIONNAIRE #4 (after first gradCPT )
result = questionnaire_routine(screen, clock)

if result is None:
    print("Questionnaire routine exited")
    running = False
else:
    print(f"Completed questionnaire instruction #{result}")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run break routine #2
result = short_break(screen, clock)
if result is None:
    print("Break routine exited")
    running = False
else:
    print("Break routine: SUCCESS")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Run rest routine #3
result = rest(screen, clock)
if result is None:
    print("Rest routine exited")
    running = False
else:
    print("Rest routine: SUCCESS")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# Run breathing calibration
result = breathing_calibration(screen, clock)
if result is None:
    print("Breathing calibration exited")
    running = False
else:
    print("Breathing calibration: SUCCESS")

# Run break routine
result = short_break(screen, clock)
if result is None:
    print("Break routine exited")
    running = False
else:
    print("Break routine: SUCCESS")


# Run social media routine
result = videos(screen, clock)
if result is None:
    print("Social media routine exited")
    running = False
else:
    print("Social media routine: SUCCESS")


# Run rest routine
result = rest(screen, clock)
if result is None:
    print("Rest routine exited")
    running = False
else:
    print("Rest routine: SUCCESS")


# Run first questionnaire
result = questionnaire_routine(screen, clock)
if result is None:
    print("Questionnaire routine exited")
    running = False
else:
    print(f"Completed questionnaire instruction #{result}")


# Run gradCPT
if running:
    print("=" * 50)
    print("GRADCPT ROUTINE")
    print("=" * 50)
    result = gradCPT_routine(screen, clock, config)
    if result is None:
        print("GradCPT routine exited")
        running = False
    elif result:
        print("GradCPT routine: SUCCESS")
    else:
        print("GradCPT routine: FAIL")
    print()


# Run second questionnaire
result = questionnaire_routine(screen, clock)
if result is None:
    print("Questionnaire routine exited")
    running = False
else:
    print(f"Completed questionnaire instruction #{result}")


# Main loop (optional - for testing after experiment)
while running:
    t = clock.get_time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                abs_time = berlin_time_now()
                rel_time = clock.get_time()
                print(f"Space pressed at {rel_time:.3f} s | Berlin time: {abs_time}")

    # Fill background
    screen.fill((0, 0, 0))
    
    # Draw something simple
    pygame.draw.rect(screen, (255, 255, 255), (350, 250, 100, 100))
    
    # Flip display to show the frame
    pygame.display.flip()

# Clean up
pygame.quit()
print("Experiment ended.")
