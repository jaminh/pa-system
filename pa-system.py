import sys
import argparse
import pymumble.pymumble_py3 as pymumble
from time import sleep
import alsaaudio as sound
import signal

class PaSystem:

	RESOLUTION = 10 # in ms
	FLOAT_RESOLUTION = float(RESOLUTION) / 1000
	SAMPLE_RATE = 48000
	CHANNELS = 1
	FORMAT = sound.PCM_FORMAT_S16_LE
	
	def __init__(self, host="127.0.0.1", port=64738, user="pa", password=None, channel=None):
		self.mumble = pymumble.Mumble(host, user=user, password=password)
		self.channel = channel 
		self.stop = False
		signal.signal( signal.SIGINT, lambda signal, frame: self.__stop() )

	def mainLoop(self):
		self.mumble.start()
		self.mumble.is_ready()

		print("Mumble connected")

		self.mumble.users.myself.mute()
		if (self.channel is not None):
			print("Requesting channel " + self.channel)
			ch = self.mumble.channels.find_by_name(self.channel)
			if (ch is not None):
				print("Switching to channel " + self.channel)
				ch.move_in()

		while(self.mumble.is_alive() and not self.stop):
			sleep(1)
			self.mumble.set_receive_sound(True)
			for user in self.mumble.users.values():
				if (user.sound.is_sound()):
					print("Got sound from user " + user["name"])
					output = sound.PCM(sound.PCM_PLAYBACK)
					output.setchannels(self.CHANNELS)
					output.setrate(self.SAMPLE_RATE)
					output.setformat(self.FORMAT)
					while(user.sound.is_sound()):
						snd = user.sound.get_sound(self.FLOAT_RESOLUTION)
						output.write(snd.pcm)

					print("Done writing audio")
					output.close()
					

		self.mumble.set_receive_sound(False)

	def __stop(self):
		print("Stop requested")
		self.stop = True

# #################################################################################
#
#
#
# #################################################################################

parser = argparse.ArgumentParser("Mumble PA System");
parser.add_argument("--host", dest="host", default="127.0.0.1", help="Hostname or IP address of the Mumble server, defaults to localhost (127.0.0.1)")
parser.add_argument("--port", dest="port", default=64738, help="Port number used by Mumble, defaults to 64738")
parser.add_argument("--user", dest="user", default="pa", help="User to connect to Mumble as, defaults to \"pa\"")
parser.add_argument("--password", dest="password", default=None, help="Password used to connect to Mumble if one is required, defaults to None")
parser.add_argument("--channel", dest="channel", default=None, help="Channel to listen on, defaults to None")

args = parser.parse_args()

app = PaSystem(host=args.host, port=args.port, user=args.user, password=args.password, channel=args.channel)
app.mainLoop()

print("Mumble client stopped")
sys.exit(0)
