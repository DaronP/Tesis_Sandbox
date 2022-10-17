from random import random, seed
from scamp import *
import random
from random import choice
import time

s = Session()

s.tempo = 180

try:
    drum = s.new_midi_part('drums', 1)
    p_bass = s.new_midi_part('Electric Bass (pick)', 2)
    d_guitar = s.new_midi_part('Distortion Guitar', 3)
except:
    drum = s.new_part('drums')
    p_bass = s.new_part('Electric Bass (pick)')
    d_guitar = s.new_part('Distortion Guitar')
    



#Negative note means: a silence with the duration of said note

def play_guitar(notas, rythm):
    tempo = s.tempo
    for n in range(len(rythm) - 1):
        if 4.0 in rythm[n] and s.tempo == tempo:
            s.tempo = s.tempo/2
        for d in range(len(notas[n])):
            if rythm[n][d] < 0.0:
                if type(notas[n][d]) == int:
                    d_guitar.play_note(notas[n][d], 0.0, (rythm[n][d]* -1))
                else:
                    d_guitar.play_chord(notas[n][d], 0.0, (rythm[n][d]* -1))
            else:
                if type(notas[n][d]) == int:
                    d_guitar.play_note(notas[n][d], 1.0, rythm[n][d])
                else:
                    d_guitar.play_chord(notas[n][d], 1.0, rythm[n][d])

def play_bass(notas, rythm):
    
    for n in range(len(rythm) - 1):
        for d in range(len(notas[n])):
            if rythm[n][d] < 0.0:
                p_bass.play_note(notas[n][d], 0.0, (rythm[n][d]* -1))
            else:
                p_bass.play_note(notas[n][d], 1.0, rythm[n][d])

def play_snare(notas = []):
    
    for n in notas:
        for d in range(len(n)):
            if n[d] < 0.0:
                drum.play_note(38, 0.0, (n[d]* -1))
            else:
                drum.play_note(38, 1.0, n[d])
        

def play_kick_drum(notas = []):
    
    for n in notas:
        for d in range(len(n)):
            if n[d] < 0.0:
                drum.play_note(36, 0.0, (n[d] * -1))
            else:
                drum.play_note(36, 1.0, n[d])

def play_cimbal(notas):
    
    for n in notas:
        for d in range(len(n)):
            if n[d] < 0.0:
                drum.play_note(58, 0.0, (n[d] * -1))
            else:
                drum.play_note(58, 1.0, n[d])

def play_hhat(notas):
    
    for n in notas:
        for d in range(len(n)):
            if n[d] < 0.0:
                drum.play_note(42, 0.0, (n[d] * -1))
            else:
                drum.play_note(42, 1.0, n[d])