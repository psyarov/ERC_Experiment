import time

class Clock:
	def __init__(self):
		self.reset()

	def reset(self):
		self._t0 = time.perf_counter()

	def get_time(self):
		return time.perf_counter() - self._t0
