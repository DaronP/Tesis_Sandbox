from random import random, seed
from abjad import Guitar
from scamp import *
import random
import time

from sqlalchemy import false


s = Session()

s.tempo = 100

d_guitar = s.new_part('Distortion Guitar')
p_bass = s.new_part('Electric Bass (pick)')
drum = s.new_midi_part('drums', 1)

for i in range(48):
    drum.play_note(36, 0.33, 0.25)
    print('Bass Drum')
for i in range(48):
    drum.play_note(37, 0.33, 0.25)
    print('Snare Rim')
for i in range(48):
    drum.play_note(38, 0.33, 0.25)
    print('Snare')
for i in range(48):
    drum.play_note(41, 0.33, 0.25)
    print('Floor Tom')
for i in range(48):
    drum.play_note(42, 0.33, 0.25)
    print('Closed Hi Hat')
for i in range(48):
    drum.play_note(44, 0.33, 0.25)
    print('Hi Hat Foot')
for i in range(48):
    drum.play_note(45, 0.33, 0.25)
    print('Low Tom')
for i in range(48):
    drum.play_note(48, 0.33, 0.25)
    print('High Tom')
for i in range(48):
    drum.play_note(46, 0.33, 0.25)
    print('Open Hi Hat')
for i in range(48):
    drum.play_note(49, 0.33, 0.25)
    print('Crash')
for i in range(48):
        drum.play_note(51, 0.33, 0.25)
        print('Ride Body')
for i in range(48):
        drum.play_note(52, 0.33, 0.25)
        print('China Cymbal')
for i in range(48):
    drum.play_note(53, 0.33, 0.25)
    print('Ride Bell')
for i in range(48):
    drum.play_note(55, 0.33, 0.25)
    print('Splash Cymbal')
for i in range(48):
    drum.play_note(58, 0.33, 0.25)
    print('Crash + Hold')