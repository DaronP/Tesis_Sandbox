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

aeolian = [2, 1, 2, 2, 1, 2]
mixolydian = [2, 2, 1, 2, 2, 1]

chords_form = [2, 4]

g_pitch = 38
b_pitch = 26

tonality = [2, 4, 6]

def play_snare(l, dur):
    for _ in range(l):
        drum.play_note(38, 0.33, dur)

def play_bass_drum(l, dur):
    for _ in range(l):
        drum.play_note(36, 0.33, dur)

def play_crash_hold(l, dur):
    for _ in range (l):
        drum.play_note(58, 0.33, dur)

def ride_bell(l, dur):
    for _ in range(l):
        drum.play_note(53, 0.33, dur)

def play_hat(l, dur):
    for _ in range(l):
        drum.play_note(42, 0.75, dur)

def play_crash(l, dur):
    for _ in range(l):
        drum.play_note(49, 0.33, dur)



s.fork(play_snare, args=[16, 1.0])
s.fork(play_bass_drum, args=[128, 0.125])
s.fork(play_hat, args=[16, 0.5])

wait(8)
s.fork(play_crash_hold, args=[16, 0.5])

wait(8)
s.fork(play_crash_hold, args=[1, 0.5])
wait(0.25)
s.fork(play_crash, args=[1, 0.5])
wait(0.25)
s.fork(play_crash_hold, args=[1, 0.5])
wait(0.5)
s.fork(play_snare, args=[128, 0.125])
s.fork(play_bass_drum, args=[128, 0.125])
s.fork(play_hat, args=[64, 0.25])
wait(16)
s.fork(play_crash, args=[1, 1])
s.fork(play_crash_hold, args=[1, 1])
s.wait_for_children_to_finish()