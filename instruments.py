from random import random, seed
from scamp import *
import random
from random import choice
import time

s = Session()

s.tempo = 240

d_guitar = s.new_part('Distortion Guitar')
p_bass = s.new_part('Electric Bass (pick)')
#drum = s.new_midi_part('drums', 1)


#Negative note means: a silence with the duration of said note

def play_guitar(notas, rythm):
    for n in range(len(notas)):
        for d in range(len(notas[n])):
            if rythm[n][d] < 0.0:
                if type(notas[n][d]) != list():
                    d_guitar.play_note(notas[n][d], 0.0, (rythm[n][d]* -1))
                else:
                    d_guitar.play_chord(notas[n][d], 0.0, (rythm[n][d]* -1))
            else:
                if type(notas[n][d]) != list():
                    d_guitar.play_note(notas[n][d], 1.0, rythm[n][d])
                else:
                    d_guitar.play_chord(notas[n][d], 1.0, rythm[n][d])

def play_guitar_chord(notes):
    d_guitar.play_chord(notes, 1.0, 1)

def play_bass(notas, rythm):
    for n in range(len(notas)):
        for d in range(len(notas[n])):
            if rythm[n][d] < 0.0:
                d_guitar.play_note(notas[n][d], 0.0, (rythm[n][d]* -1))
            else:
                d_guitar.play_note(notas[n][d], 1.0, rythm[n][d])

def play_snare(notas = []):
    for n in notas:
        for d in range(len(n)):
            if n[d] < 0.0:
                drum.play_note(38, 0.0, (n[d]* -1))
            else:
                drum.play_note(38, 0.33, n[d])
        

def play_kick_drum(notas = []):

    for n in notas:
        for d in range(len(n)):
            if n[d] < 0.0:
                drum.play_note(36, 0.0, (n[d] * -1))
            else:
                drum.play_note(36, 0.33, n[d])

def play_cimbal(notas):
    for n in notas:
        for d in range(len(n)):
            if n[d] < 0.0:
                drum.play_note(58, 0.0, (n[d] * -1))
            else:
                drum.play_note(58, 0.33, n[d])

def play_china_cimbal(notas):
    for n in notas:
        for d in range(len(n)):
            drum.play_note(52, 0.75, n[d])

def play_crash_hold(notas = []):
    for n in notas:
        for d in range(len(n)):
            drum.play_note(49, 0.33, n[d])

def ride_bell(dur = []):
    drum.play_note(53, 0.33, dur)

def play_hhat(notas):
    for n in notas:
        for d in range(len(n)):
            if n[d] < 0.0:
                drum.play_note(42, 0.0, (n[d] * -1))
            else:
                drum.play_note(42, 0.33, n[d])

def play_open_hhat(dur):
    drum.play_note(55, 0.33, dur)