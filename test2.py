from random import random, seed
from abjad import Guitar
from scamp import *
import random
import time


s = Session()

s.tempo = 100

d_guitar = s.new_part('Distortion Guitar')
p_bass = s.new_part('Electric Bass (pick)')
drum = s.new_midi_part('drums', 1)

aeolian = [2, 1, 2, 2, 1, 2]

chords_form = [2, 4]

pitch = 45

'''for e in range(len(aeolian) + 1):
        d_guitar.play_note(pitch, 1.0, 0.5)
        try:
            pitch = pitch + aeolian[e]
        except:
            pass'''

pitch = 33


def make_chords(pitch_f):
    chords = []
    chords.append(pitch_f)
    for i in chords_form:
        pitch_sum = pitch_f + sum(aeolian[:i])
        '''if pitch_sum > (pitch + 10): 
            pitch_sum = pitch_sum - sum(aeolian)'''
            
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
    notes = []
    for i in tonalities:
        tone_pitch = pitch + sum(aeolian[: i - 1]) 
        notes.append(make_chords(tone_pitch))

    for note in notes:            
        for _ in range(8):
            for n in note:
                #print(n)            
                d_guitar.play_note(n, 1.0, 0.25)
        for n in range(len(note)):
            d_guitar.play_note(note[len(note) - n - 1], 1.0, 0.25)

def play_hat():
    for _ in range(56):
        drum.play_note(42, 0.75, 0.5)


def play_backbeat():
    doub = False
    for i in range(24):
        if i % 2 == 0:
            if i % 4 == 0:
                drum.play_note(36, 0.33, 0.125)
                drum.play_note(36, 0.33, 0.125)
                drum.play_note(36, 0.33, 0.125)
                drum.play_note(36, 0.33, 0.125)
                drum.play_note(36, 0.33, 0.125)
                drum.play_note(36, 0.33, 0.125)
                drum.play_note(36, 0.33, 0.125)
                drum.play_note(36, 0.33, 0.125)
            else:
                drum.play_note(36, 0.33, 0.25)
                drum.play_note(36, 0.33, 0.25)
                drum.play_note(36, 0.33, 0.125)
                drum.play_note(36, 0.33, 0.125)
                drum.play_note(36, 0.33, 0.25)
                
        else:
            
            if doub:
                drum.play_note(38, 0.33, 0.5)
                drum.play_note(38, 0.33, 0.5)
                doub = False
            else:
                drum.play_note(38, 0.33, 1.0)
                doub = True
                
            


tonality = [1, 4, 5, 1]

fork(play_hat)
wait(4)
fork(play_backbeat)
fork(a_minor_notesv4, args=[pitch, tonality])
fork(a_minor_notesv5, args=[21, tonality])
wait_for_children_to_finish()