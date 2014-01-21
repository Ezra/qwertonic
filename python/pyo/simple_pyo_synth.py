#http://waterpigs.co.uk/articles/simple-pyo-synth/
#cc-by-sa
from pyo import *

# Set Up Server
s = Server()
s.setMidiInputDevice(2) # Change as required
s.boot()
s.start()

# Set Up MIDI
midi = Notein()

# ADSR
amp = MidiAdsr(midi[velocity])

# Pitch
pitch = MToF(midi[pitch])

# Table
wave = SquareTable()

# Osc
osc = Osc(wave, freq=pitch, mul=amp)

# FX
verb = Freeverb(osc).out()

### Go
osc.out()
s.gui(locals()) # Prevents immediate script termination.
