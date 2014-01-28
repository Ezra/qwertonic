#!/usr/bin/env python

# qwertonic-py
# a prototype implementation of the qwertonic keyboard
# (http://www.qwertonic.com/)
# version 0.2dev
#
# requires pyo
# https://code.google.com/p/pyo/
#
# files: qwertonic.py (this file), music.py


# for gui and input
from Tkinter import *
from PIL import ImageTk, Image

# for pyo music server
print "Qwertonic Keyboard version 0.2dev, with ", # can't suppress pyo output, so use it
from music import *
import time

# for logging
import logging as log
import argparse

#logging
parser = argparse.ArgumentParser(description="play music with qwerty keyboard")
parser.add_argument("-v", "--verbosity", help="increase output verbosity",
        action="count", default=0)
args = parser.parse_args()    

if args.verbosity >= 2:
    log.basicConfig(level=log.DEBUG,
            format="%(asctime)s: %(message)s")
    log.info("Qwertonic vverbose event output")
elif args.verbosity == 1:
    log.basicConfig(level=log.INFO,
            format="%(msecs)03d: %(message)s")
    log.info("Qwertonic event output milliseconds")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")

#start server
s = musicServer()
time.sleep(0.5)
startServer(s)

# http://www.seventhstring.com/resources/notefrequencies.html
# for greater precision (but slightly narrower on the ends),
# see http://mdoege.github.io/PySynth/
# for general formula,
# see http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html
#
#     C     C#    D     Eb    E     F     F#    G     G#    A     Bb    B
#   0 16.35 17.32 18.35 19.45 20.60 21.83 23.12 24.50 25.96 27.50 29.14 30.87
#   1 32.70 34.65 36.71 38.89 41.20 43.65 46.25 49.00 51.91 55.00 58.27 61.74
#   2 65.41 69.30 73.42 77.78 82.41 87.31 92.50 98.00 103.8 110.0 116.5 123.5
#   3 130.8 138.6 146.8 155.6 164.8 174.6 185.0 196.0 207.7 220.0 233.1 246.9
#   4 261.6 277.2 293.7 311.1 329.6 349.2 370.0 392.0 415.3 440.0 466.2 493.9
#   5 523.3 554.4 587.3 622.3 659.3 698.5 740.0 784.0 830.6 880.0 932.3 987.8
#   6 1047  1109  1175  1245  1319  1397  1480  1568  1661  1760  1865  1976
#   7 2093  2217  2349  2489  2637  2794  2960  3136  3322  3520  3729  3951
#   8 4186  4435  4699  4978  5274  5588  5920  6272  6645  7040  7459  7902

freqs = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87,
         32.70, 34.65, 36.71, 38.89, 41.20, 43.65, 46.25, 49.00, 51.91, 55.00, 58.27, 61.74,
         65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.8, 110.0, 116.5, 123.5,
         130.8, 138.6, 146.8, 155.6, 164.8, 174.6, 185.0, 196.0, 207.7, 220.0, 233.1, 246.9,
         261.6, 277.2, 293.7, 311.1, 329.6, 349.2, 370.0, 392.0, 415.3, 440.0, 466.2, 493.9,
         523.3, 554.4, 587.3, 622.3, 659.3, 698.5, 740.0, 784.0, 830.6, 880.0, 932.3, 987.8,
         1047,  1109,  1175,  1245,  1319,  1397,  1480,  1568,  1661,  1760,  1865,  1976,
         2093,  2217,  2349,  2489,  2637,  2794,  2960,  3136,  3322,  3520,  3729,  3951,
         4186,  4435,  4699,  4978,  5274,  5588,  5920,  6272,  6645,  7040,  7459,  7902]

# oct*12+note
# octaves: standard octave numbers from 0 to 8 (middle C and A are in row 4)
# notes:
#  C C#  D Eb  E  F F#  G G#  A Bb  B
#  0  1  2  3  4  5  6  7  8  9 10 11

# duration 0 means we'll specify the end with stop()
notes = map((lambda frequency: note(frequency, duration=0)), freqs)

# Return a map from key to note
def make_key_mapping(key_list, start_note_num):
    mapping = {}
    for i in range(len(key_list)):
        mapping[key_list[i]] = notes[start_note_num+(2*i)]
    return mapping

key_mapping = make_key_mapping(['z','x','c','v','b','n','m',',','.','/'],
              4*12+4)
key_mapping.update(make_key_mapping(['a','s','d','f','g','h','j','k','l',';','\''],
              4*12+9))
key_mapping.update(make_key_mapping(['q','w','e','r','t','y','u','i','o','p','[',']'],
              5*12+2))
key_mapping.update(make_key_mapping(['1','2','3','4','5','6','7','8','9','0','-','='],
              5*12+7))

# tkinter loop
# adapted from http://stackoverflow.com/questions/2138518/python-bind-allow-multiple-keys-to-be-pressed-simultaniously
class QwertonicKeyboard:
    def __init__(self):
        # keys currently pressed (as characters, per Tkinter)
        self.pressed = {}
        self.afterId = {}

        self._create_ui()

    def start(self):
        self.root.mainloop()

    def _create_ui(self):
        self.root = Tk()
        self.canvas = Canvas(self.root)

        self.canvas.pack(side="top", fill="both", expand="true")

        img = Image.open('resources/qwertonic-illustration.gif')
        self.root.geometry('%dx%d' % (img.size[0],img.size[1]))
        self.image = ImageTk.PhotoImage(img)
        label=Label(self.root, image=self.image)
        label.place(x=0,y=0,width=img.size[0],height=img.size[1])
        self.root.title("Qwertonic")

        self._set_bindings()


    def _animate(self):
        self.root.after(10, self._animate)

    def _set_bindings(self):
        for key in key_mapping:
            self.root.bind("<KeyPress-%s>" % key, self._pressed)
            self.root.bind("<KeyRelease-%s>" % key, self._released)
            self.pressed[key] = False
            self.afterId[key] = None

    def _pressed(self, event):
        key = event.char
        log.debug('%r press?' % key)
        if (key in self.afterId) and (self.afterId[key] != None):
            self.root.after_cancel( self.afterId[key] )
            self.afterId[key] = None
        else:
            log.info('%r pressed' % key)
            if (key in self.pressed) and not (self.pressed[key]):
                self.pressed[key] = True
                try:
                    note = key_mapping[key]
                except KeyError:
                    pass
                else:
                    note.play()

    def _released(self, event):
        key = event.char
        log.debug('%r release?' % key)
        if (key in self.afterId):
            self.afterId[key] = self.root.after_idle( self.process_release, event )
    def process_release(self, event):
        key = event.char
        log.info('%r released' % key)
        if (key in self.pressed) and (self.pressed[key]):
            self.pressed[event.char] = False
            key = event.char
            try:
                note = key_mapping[key]
            except KeyError:
                pass
            else:
                note.stop()
        self.afterId[key] = None


if __name__ == "__main__":
    qk = QwertonicKeyboard()
    qk.start()
