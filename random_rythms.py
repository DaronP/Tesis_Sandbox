from random import random, seed
#from abjad import Guitar
from scamp import *
import random
import time


s = Session()

s.tempo = 140

'''d_guitar = s.new_part('Distortion Guitar')
p_bass = s.new_part('Electric Bass (pick)')'''
drum = s.new_midi_part('drums', 1)

d_file = open('Drum Map.txt', 'r')
drum_kit = d_file.readlines()
for i in range(len(drum_kit)):
    percussion = drum_kit[i]
    percussion = percussion.replace('\n', '')
    percussion = percussion.split(' - ')
    percussion[0] = int(percussion[0])
    drum_kit[i] = percussion
    #print(drum_kit[i])

aeolian = [2, 1, 2, 2, 1, 2]
mixolydian = [2, 2, 1, 2, 2, 1]
dorian = [2, 1, 2, 2, 2, 1]

chords_form = [2, 4]

g_pitch = 38
b_pitch = 26

tonality = [2, 4, 6]


compas_hihat = []

n_compases = input('Ingresar el numero de compases: ')

penta = []
hh_penta = []

for i in range(int(n_compases)):
    compas = []
    sum_compas = 0
    for j in range(4):
        sum_compas = sum(compas)
        nota = 1/pow(2, random.randrange(2, 6))
        nota = nota/0.25
        compas.append(nota)

        if nota == 0.5:
            compas.append(nota)
            j += 1
        if nota == 0.25:
            compas.append(nota)
            compas.append(nota)
            compas.append(nota)
            j += 1
        if nota == 0.125:
            compas.append(nota)
            compas.append(nota)
            compas.append(nota)
            compas.append(nota)
            compas.append(nota)
            compas.append(nota)
            compas.append(nota)
            j += 1
        
        if sum_compas >= 4.0:
            i += 1
            break
    
    penta.append(compas)
    repetition = bool(random.getrandbits(1))
    if repetition:
        penta.append(compas)
        penta.append(compas)
        penta.append(compas)

for i in range(len(penta)):
    compas = []
    for j in range(4):
        compas.append(1.0)
    hh_penta.append(compas)

print('-----------------------------------------------------------------------------------------------------')
for i in penta:
    print(i)
    su = 0.0
    for r in i:
        su += r
    print(su)
print(len(penta))

def play_snare(notas = []):
    for n in notas:
        for d in range(len(n)):
            if not d % 2:
                drum.play_note(38, 0.33, n[d])

            else: 
                drum.play_note(38, 0, n[d])

def play_bass_drum(notas = []):
    for n in notas:
        for d in range(len(n)):
            drum.play_note(36, 0.33, n[d])

def play_crash_hold(dur = []):
    drum.play_note(58, 0.33, dur)

def ride_bell(dur = []):
    drum.play_note(53, 0.33, dur)

def play_hhat(notas):
    for n in notas:
        for d in range(len(n)):
            drum.play_note(42, 0.75, n[d])

def play_crash(dur):
    drum.play_note(49, 0.33, dur)



s.fork(play_hhat, args=[hh_penta]) 
s.fork(play_snare, args=[penta])
s.fork(play_bass_drum, args=[penta])

s.wait_for_children_to_finish()