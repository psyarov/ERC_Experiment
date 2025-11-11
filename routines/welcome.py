# routines/welcome.py
import pygame

class Button:
	def __init__(self, x, y, width, height, color, text, text_color=(255, 255, 255)):
		self.rect = pygame.Rect(x, y, width, height)
		self.color = color
		self.text = text
		self.text_color = text_color
		self.font = pygame.font.Font(None, 36)
	
	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)
		pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)  # Border
		
		text_surface = self.font.render(self.text, True, self.text_color)
		text_rect = text_surface.get_rect(center=self.rect.center)
		surface.blit(text_surface, text_rect)
	
	def is_clicked(self, pos):
		return self.rect.collidepoint(pos)


def welcome_routine(screen, clock):
	"""
	Display welcome screen with red and blue buttons.
	Returns True if red button is pressed (success), False if blue button is pressed (fail).
	Returns None if ESC is pressed or window is closed.
	"""
	# Screen states
	STATE_WELCOME = "welcome"
	STATE_SUCCESS = "success"
	STATE_FAIL = "fail"
	
	current_state = STATE_WELCOME
	
	# Create buttons
	red_button = Button(250, 350, 120, 60, (200, 0, 0), "RED")
	blue_button = Button(430, 350, 120, 60, (0, 0, 200), "BLUE")
	
	# Fonts
	font_large = pygame.font.Font(None, 48)
	font_medium = pygame.font.Font(None, 36)
	
	running = True
	result = None
	show_result_until = None  # Timestamp when to exit after showing result
	pygame_clock = pygame.time.Clock()  # For frame rate control
	
	while running:
		t = clock.get_time()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return None
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return None
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if current_state == STATE_WELCOME:
					if red_button.is_clicked(event.pos):
						current_state = STATE_SUCCESS
						result = True
						show_result_until = pygame.time.get_ticks() + 1500
						print(f"Red button clicked at {clock.get_time():.3f} s - Success!")
					elif blue_button.is_clicked(event.pos):
						current_state = STATE_FAIL
						result = False
						show_result_until = pygame.time.get_ticks() + 1500
						print(f"Blue button clicked at {clock.get_time():.3f} s - Epic Fail!")
		
		# Check if we should exit after showing result
		if show_result_until is not None and pygame.time.get_ticks() >= show_result_until:
			running = False
		
		# Fill background
		screen.fill((0, 0, 0))
		
		# Draw based on current state
		if current_state == STATE_WELCOME:
			# Welcome screen
			text1 = font_large.render("Welcome to the experiment!", True, (255, 255, 255))
			text2 = font_medium.render("Press the red button to continue", True, (255, 255, 255))
			
			text1_rect = text1.get_rect(center=(400, 200))
			text2_rect = text2.get_rect(center=(400, 260))
			
			screen.blit(text1, text1_rect)
			screen.blit(text2, text2_rect)
			
			# Draw buttons
			red_button.draw(screen)
			blue_button.draw(screen)
		
		elif current_state == STATE_SUCCESS:
			# Success screen
			text = font_large.render("Success!", True, (0, 255, 0))
			text_rect = text.get_rect(center=(400, 300))
			screen.blit(text, text_rect)
		
		elif current_state == STATE_FAIL:
			# Fail screen
			text = font_large.render("Epic Fail...", True, (255, 0, 0))
			text_rect = text.get_rect(center=(400, 300))
			screen.blit(text, text_rect)
		
		# Flip display to show the frame
		pygame.display.flip()
	
	return result
