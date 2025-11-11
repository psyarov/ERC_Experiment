import os
import pygame
from core.clock import Clock
from core.fps_estimator import FPSEstimator
from core.gradcpt_config import GradCPTConfig
from datetime import datetime, timezone, timedelta
from routines.welcome import welcome_routine
from routines.gradcpt import gradCPT_routine

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



# BACKUP 09-11-2025 23:57
# import os
# import pygame

# from core.clock import Clock
# from datetime import datetime, timezone, timedelta
# from routines.welcome import welcome_routine
# from routines.gradcpt import gradCPT_routine

# # Init
# print("Launching main.py...")
# print("Initializing pygame...")
# pygame.init()

# print("Creating screen...")
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Experiment Window")

# print("Setting up clock...")
# clock = Clock()
# BERLIN_TZ = timezone(timedelta(hours=1))

# def berlin_time_now():
# 	return datetime.now(BERLIN_TZ).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

# running = True

# print("Experiment running!\n\nHELLO, WORLD!\n\n")


# # Run welcome routine

# print("Starting welcome routine...")
# result = welcome_routine(screen, clock)

# if result is None:
# 	print("Welcome routine exited (ESC or window closed)")
# 	running = False
# elif result:
# 	print("Welcome routine: SUCCESS - continuing with experiment")
# else:
# 	print("Welcome routine: FAIL - continuing with experiment")


# # Run gradCPT
# print("Starting gradCPT routine...")

# result = gradCPT_routine(screen, clock)
# if result is None:
#     print("Morphing routine exited")
#     running = False
# elif result:
#     print("Morphing routine: SUCCESS")
# else:
#     print("Morphing routine: FAIL")

# # Main loop

# while running:
# 	t = clock.get_time()
	
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			running = False
# 		elif event.type == pygame.KEYDOWN:
# 			if event.key == pygame.K_ESCAPE:
# 				running = False
# 			elif event.key == pygame.K_SPACE:
# 				abs_time = berlin_time_now()
# 				rel_time = clock.get_time()
# 				print(f"Space pressed at {rel_time:.3f} s | Berlin time: {abs_time}")

	
# 	# Fill background
# 	screen.fill((0, 0, 0))

# 	# Draw something simple
# 	pygame.draw.rect(screen, (255, 255, 255), (350, 250, 100, 100))

# 	# Flip display to show the frame
# 	pygame.display.flip()

# # Clean up
# pygame.quit()
# print("Experiment ended.")



# while running:
# 	t = clock.get_time()
# 	print(f"time: {t}")
