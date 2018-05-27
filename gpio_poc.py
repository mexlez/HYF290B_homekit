import RPi.GPIO as g
import time, threading

# Trigger off of LED- going LOW (is LOW for ~6ms)
# Check if LED+ == HI

# LED common mode pins; shared by LEDs
LED_common_1 = 16
LED_common_2 = 18

# Button lines; active low for at least 10ms
BTN_power = 22
#included only for completeness; turning the lights off will break status checking
BTN_light = 24
BTN_oscillate = 26
BTN_speed = 32
BTN_timer = 36

# LED high lines; used along with LED common lines to infer statuses

# Speed LEDs
STAT_SP1_2 = 11
STAT_SP3_4 = 13
STAT_SP5_6 = 15
STAT_SP7_8 = 19

# Timer LEDs
STAT_T1_2 = 21
STAT_T4_8 = 23

g.setmode(g.BOARD)


class LED_watcher():
	def __init__(self, hi_pin, common_pin, name, phase=False):
		self.was_active = False
		self.active = False

		self.name = name
		self.hi_pin = hi_pin
		self.lo_pin = common_pin
		self.phase = phase

		g.setup(self.hi_pin, g.IN)
		g.setup(self.lo_pin, g.IN)
		try:
			g.add_event_detect(self.lo_pin, g.FALLING, bouncetime=3)
		except Exception as e:
			pass 
		g.add_event_callback(self.lo_pin, self.callback)
		self.timer = None

	def restart_timer(self, interval):
		if self.timer:
			self.timer.cancel()
		self.timer = threading.Timer(interval, self.timer_cb)
		self.timer.start()

	def timer_cb(self):
		if self.active:
			self.active = False
			print("{}:: OFF".format(self.name))

	def callback(self, channel):
		l = g.input(self.lo_pin)
		h = g.input(self.hi_pin)
		#l = g.input(self.lo_pin)
		#if self.phase:
			#time.sleep(0.001)
			#h = g.input(self.hi_pin)
		if h and not l:
			self.restart_timer(0.01)
			if self.active == False:
				self.active = True
				print("{}:: ON".format(self.name))
		#print("{}::{}".format(h, l))

class button_pusher():
	def __init__(self, pin, name):
		self.name = name
		self.pin = pin
		g.setup(self.pin, g.IN)

	def push(self):
		g.setup(self.pin, g.OUT)
		g.output(self.pin, False)
		time.sleep(0.1)
		g.setup(self.pin, g.IN)
		print("Button {} pushed!".format(self.name))	
	
LED_watcher(STAT_SP1_2, LED_common_2, "Speed 1")
LED_watcher(STAT_SP1_2, LED_common_1, "Speed 2")
LED_watcher(STAT_SP3_4, LED_common_2, "Speed 3")
LED_watcher(STAT_SP3_4, LED_common_1, "Speed 4")
LED_watcher(STAT_SP5_6, LED_common_2, "Speed 5")
LED_watcher(STAT_SP5_6, LED_common_1, "Speed 6")
LED_watcher(STAT_SP7_8, LED_common_2, "Speed 7")
LED_watcher(STAT_SP7_8, LED_common_1, "Speed 8")


LED_watcher(STAT_T1_2, LED_common_2, "Timer 1h", True)
LED_watcher(STAT_T1_2, LED_common_1, "Timer 2h", True)
LED_watcher(STAT_T4_8, LED_common_2, "Timer 4h", True)
LED_watcher(STAT_T4_8, LED_common_1, "Timer 8h", True)

power = button_pusher(BTN_power, "Power")
speed = button_pusher(BTN_speed, "Speed")
oscillate = button_pusher(BTN_oscillate, "Oscillate")
timer = button_pusher(BTN_timer, "Timer")


print("Commands:")
print("Power: p")
print("Speed: s")
print("Oscillate: o")
print("Timer: t")
print("Quit: q")
while True:
	c = raw_input()
	if c == "p":
		power.push()
	elif c == "s":
		speed.push()
	elif c == "o":
		oscillate.push()
	elif c == "t":
		timer.push()
	elif c == "q":
		g.cleanup()
		quit()
	else:
		print("Invalid command '{}'".format(c))

