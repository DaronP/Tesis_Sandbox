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


'''for e in range(len(aeolian) + 1):
        d_guitar.play_note(pitch, 1.0, 0.5)
        try:
            pitch = pitch + aeolian[e]
        except:
            pass'''

def play_crash():
    drum.play_note(49, 0.33, 1)

def play_crash_hold():
    drum.play_note(58, 0.33, 1)

def play_snare():
    drum.play_note(38, 0.33, 0.5)

def play_bass_drum():
    drum.play_note(36, 0.33, 0.5)

def ride_bell(l):
    print('bellzzzzz')
    for _ in range(l):
        drum.play_note(53, 0.33, 0.5)
    
    s.fork(play_snare)
    s.fork(play_bass_drum)
    play_bass_drum()
    s.fork(play_crash)
    s.fork(play_crash_hold)
    s.fork(play_bass_drum)
    

def play_hat(l):
    for _ in range(l):
        drum.play_note(42, 0.75, 0.5)
    s.fork(ride_bell, args=[16])


def make_chords(pitch_f, flag=False):
    chords = []
    chords.append(pitch_f)
    if not flag:
        for i in chords_form:
            pitch_sum = pitch_f + sum(mixolydian[:i])         
            chords.append(pitch_sum)
    else:
        mix = mixolydian[1:]
        for i in chords_form:
            pitch_sum = pitch_f + sum(mix[:i])         
            chords.append(pitch_sum)
    
    return chords

def bass_notes(pitch, tonalities):
    notes = []
    for i in tonalities:
        tone_pitch = pitch + sum(mixolydian[: i - 1]) 
        if i != 1:
            flag = True
        else: 
            flag = False
        notes.append(make_chords(tone_pitch, flag))
        
    for j in range(4):
        print(j)
        for note in range(len(notes)):
            for n in range(len(notes[note])):
                if n == 0:
                    for _ in range(8):
                        p_bass.play_note(notes[note][n], 1.0, 0.25)
                
                else:
                    for _ in range(3):
                        p_bass.play_note(notes[note][n], 1.0, 0.25)



def guitar_notes(pitch, tonalities):
    notes = []            
    for i in tonalities:
        tone_pitch = pitch + sum(mixolydian[: i - 1])
        if i != 1:
            flag = True
        else: 
            flag = False
        notes.append(make_chords(tone_pitch, flag))

    for j in range(3):
        if j >= 2:
            s.tempo = 60
        for n in range(4):
            if n == 0 and j != 0:
                for i in range(2):
                    for _ in range(4):  
                        c = [notes[0][0], notes[0][1]]
                        d_guitar.play_chord(c, 1.0, 0.25)
                        d_guitar.play_chord(c, 1.0, 0.25)

                    for _ in range(3):  
                        c = [notes[0][0], notes[0][1]]
                        d_guitar.play_chord(c, 1.0, 0.25)
                        d_guitar.play_chord(c, 1.0, 0.25)
                    d_guitar.play_note(notes[1][1], 1.0, 0.25)
                    d_guitar.play_note(notes[1][-1], 1.0, 0.25)


            if s.tempo == 100:
                for _ in range(3):  
                    c = [notes[0][0], notes[0][1]]
                    d_guitar.play_chord(c, 1.0, 0.125)
                    d_guitar.play_chord(c, 1.0, 0.125)  
                    d_guitar.play_chord(c, 1.0, 0.125)
                    wait(0.125)
            else:
                for _ in range(3):  
                    c = [notes[0][0], notes[0][1]]
                    d_guitar.play_chord(c, 1.0, 0.25)
                    d_guitar.play_chord(c, 1.0, 0.25)
                
            try:
                if n % 2 != 0:
                    d_guitar.play_note(notes[-1][-1], 1.0, 0.25)
                    d_guitar.play_note(notes[-1][1], 1.0, 0.25)
                else:
                    d_guitar.play_note(notes[1][1], 1.0, 0.25)
                    d_guitar.play_note(notes[1][-1], 1.0, 0.25)
            except:
                pass




def play_backbeat():
    doub = False
    for i in range(40):
        if i % 2 == 0:

            if i % 4 == 0:
                for _ in range(8):
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
    
                
            
g_pitch = 38
b_pitch = 26

tonality = [2, 4, 6]

start = time.time()
s.fork(play_hat, args=[70])
wait(4)
s.fork(play_backbeat)
s.fork(guitar_notes, args=[g_pitch, tonality])

s.fork(bass_notes, args=[b_pitch, tonality])
s.wait_for_children_to_finish()
print(time.time() - start)