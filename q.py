#!/usr/bin/env python
#an attempt at a simple keyboard-to-notes

from music import *
import time

s = musicServer()
startServer(s)

#n = note()

notes = map( lambda frequency: note(frequency), [440, 880])


time.sleep(1)
notes[0].play()
time.sleep(1)
notes[1].play()
time.sleep(1)
notes[0].play()

guiMusicServer(s)
