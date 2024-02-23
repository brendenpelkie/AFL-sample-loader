import RPi.GPIO


class PiGPIO():

	def __init__(self,channels,mode='BCM',pull_dir='UP'):
		'''
		Initializes GPIO pins in channels and maps their values to a local dict.


		Params:
		channels (dict):
			mapping of pin id to load name, e.g. {0:'arm_up',1:'arm_down'}
		mode (str, 'BCM' or 'BOARD', default BCM):
			pin numbering scheme to use
		pull_dir (str or dict, default 'up')
			if string, 'UP' or 'DOWN' direction to pull all pins
			if dict, key = pin number, val = 'UP' or 'DOWN'

		'''
		self.channels = channels

		self.state = {}
		if mode == 'BCM':
			RPi.GPIO.setmode(RPi.GPIO.BCM)
		elif mode == 'BOARD':
			RPi.GPIO.setmode(RPi.GPIO.BOARD)
		else:
			raise ValueError('invalid mode in GPIORelay')

		if type(pull_dir) != dict:
			if pull_dir == 'UP':
				pull_dir = {key:'UP' for key,val in self.channels.items()}
			elif pull_dir == 'DOWN':
				pull_dir = {key:'DOWN' for key,val in self.channels.items()}
			else:
				raise ValueError('invalid pull_dir in GPIORelay')
		#Setup pins:

		for key,val in self.channels.items():
			if pull_dir[key] == 'UP':
				RPi.GPIO.setup(key,RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_UP)
			elif pull_dir[key] == 'DOWN':
				RPi.GPIO.setup(key,RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
			else:
				raise ValueError('invalid pull_dir in GPIORelay')
			RPi.GPIO.add_event_detect(key,RPi.GPIO.BOTH,callback=self.eventcb)#,bouncetime=200)



		self.ids = {val:key for key,val in self.channels.items()}

		#do an initial read of all the pin state and create self.state which maps name to val
		for key,val in self.channels.items():
			self.state[val] = RPi.GPIO.input(key)
	def eventcb(self,channel):
		'''
		In response to an edge detect, read a channel and update the local state dict.

		'''
		self.state[self.channels[channel]] = RPi.GPIO.input(channel)

