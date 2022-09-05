from random import seed
from abjad import Guitar
from scamp import *
import numpy as np
import time


s = Session()

s.tempo = 100

d_guitar = s.new_part('Distortion Guitar')
p_bass = s.new_part('Electric Bass (pick)')

aeolian = [2, 1, 2, 2, 1, 2]

chords_form = [2, 4]

pitch = 45

for e in range(len(aeolian) + 1):
        d_guitar.play_note(pitch, 1.0, 0.5)
        try:
            pitch = pitch + aeolian[e]
        except:
            pass

pitch = 45


def make_chords(pitch_f):
    chords = []
    chords.append(pitch_f)
    for i in chords_form:
        pitch_sum = pitch_f + sum(aeolian[:i])
        if pitch_sum > (pitch + 10): 
            pitch_sum = pitch_sum - sum(aeolian)
            
        chords.append(pitch_sum)
    
    return chords

def a_minor_notesv5(pitch, tonalities):
    for i in tonalities:
        tone_pitch = pitch + sum(aeolian[: i - 1]) 
        notes = make_chords(tone_pitch)
        
        for n in range(len(notes)):
            #print(n)
            if n == 0:
                for _ in range(16):
                    p_bass.play_note(notes[n], 1.0, 0.25)
            
            else:
                for _ in range(4):
                    p_bass.play_note(notes[n], 1.0, 0.25)

def a_minor_notesv4(pitch, tonalities):
    for i in tonalities:
        tone_pitch = pitch + sum(aeolian[: i - 1]) 
        notes = make_chords(tone_pitch)

        for _ in range(8):
            for n in notes:
                #print(n)            
                d_guitar.play_note(n, 1.0, 0.25)

def a_minor_notesv3(pitch, tonalities):
    for i in tonalities:
        tone_pitch = pitch + sum(aeolian[: i - 1]) 
        notes = make_chords(tone_pitch)

        for _ in range(3):
            for n in notes:
                print(n)            
                d_guitar.play_note(n, 1.0, 0.5)

def a_minor_notesv2(pitch, tonalities):
    for i in tonalities:
        tone_pitch = pitch + sum(aeolian[: i - 1]) 
        notes = make_chords(tone_pitch)

        for n in notes:
            print(n)
            for _ in range(3):
                d_guitar.play_note(n, 1.0, 0.5)

def a_minor_notesv1(pitch, tonalities):
    for i in tonalities:
        tone_pitch = pitch + sum(aeolian[: i - 1]) 
        notes = make_chords(tone_pitch)

        for n in notes:
            print(n)
            d_guitar.play_note(n, 1.0, 0.5)

def a_minor_chords(pitch, tonalities):
    for i in tonalities:
        tone_pitch = pitch + sum(aeolian[: i - 1])
        
        chords = make_chords(tone_pitch)

        print(chords)

        d_guitar.play_chord(chords, 1.0, 0.5)
            
            
tonality = [1, 4, 5, 1]
#a_minor_chords(pitch=pitch, tonalities=tonality)
#a_minor_notesv1(pitch=pitch, tonalities=tonality)
#a_minor_notesv2(pitch=pitch, tonalities=tonality)
#a_minor_notesv3(pitch=pitch, tonalities=tonality)
#a_minor_notesv4(pitch=pitch, tonalities=tonality)
#a_minor_notesv5(pitch=pitch, tonalities=tonality)
fork(a_minor_notesv4, args=[pitch, tonality])
fork(a_minor_notesv5, args=[33, tonality])

wait_for_children_to_finish()