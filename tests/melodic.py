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
dorian = [2, 1, 2, 2, 2, 1]

chords_form = [2, 4]

g_pitch = 38
b_pitch = 26

tonality = [2, 4, 6]

def make_chords(pitch_f, flag=False):
    chords = []
    chords.append(pitch_f)
    if not flag:
        for i in chords_form:
            pitch_sum = pitch_f + sum(dorian[:i])         
            chords.append(pitch_sum)
    else:
        mix = dorian[1:]
        for i in chords_form:
            pitch_sum = pitch_f + sum(mix[:i])         
            chords.append(pitch_sum)
    
    return chords

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


def play_guitar(l, pitch, tonalities):
    notes = []            
    for i in tonalities:
        tone_pitch = pitch + sum(dorian[: i - 1])
        if i != 1:
            flag = True
        else: 
            flag = False
        notes.append(make_chords(tone_pitch, flag))
    
    high_notes = []            
    for i in tonalities:
        tone_pitch = (pitch + 12) + sum(dorian[: i - 1])
        if i != 1:
            flag = True
        else: 
            flag = False
        high_notes.append(make_chords(tone_pitch, flag))
    
    for i in range(int(l/2)):
        for j in high_notes:
            for _ in range(3):
                for k in range(3):
                    d_guitar.play_note(j[k], 1.0, 0.33)
    

    s.tempo = 90


    for i in range(l):
        for _ in range(3):
            d_guitar.play_chord([notes[0][0], notes[0][1]], 1.0, 0.33)
        
        if i % 2 == 0:
            for j in range(4):
                if j % 2 == 0:
                    d_guitar.play_note(high_notes[1][0], 1.0, 0.75)
                    d_guitar.play_note(notes[0][0], 1.0, 0.25)
                else:
                    d_guitar.play_note(high_notes[1][0], 1.0, 0.1)
        
        else:
            for j in range(4):
                if j % 2 == 0:
                    d_guitar.play_note(high_notes[2][0], 1.0, 0.75)
                    d_guitar.play_note(notes[0][0], 1.0, 0.25)

                else: 
                    d_guitar.play_note(high_notes[2][0], 1.0, 1)
        
            d_guitar.play_chord([notes[2][0], notes[2][1]], 1.0, 0.25)
            d_guitar.play_chord([notes[2][0], notes[2][1]], 1.0, 0.25)


s.fork(play_guitar, args=[4, 38, tonality])
s.wait_for_children_to_finish()
