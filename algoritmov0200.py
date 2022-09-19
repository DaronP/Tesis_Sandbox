from random import random, seed
from scamp import *
import random
from random import choice
import time

s = Session()

s.tempo = 240

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


def Intro():
    intro = {'hi-hat': [],
             'crash': [],
             'snare': [],
             'b_drum': [],
             }



def Verso():
    pass

def Coro():
    pass

def Outtro():
    pass


def Rola():
    #Tendra intro?
    have_intro = 1#random.getrandbits(1)
    have_outtro = random.getrandbits(1)
    song_structure = []
    
    if have_intro == 1:
        song_structure.append('Intro')
    
    #Generical song structure
    #Verse
    song_structure.append('Verse')
    #Chorus
    song_structure.append('Chorus')
    #Will second verse will be different?
    different_verse = random.getrandbits(1)
    if different_verse:
        song_structure.append('D_Verse')
    else:
        #Same verse
        song_structure.append('Verse')
    song_structure.append('Chorus')
    song_structure.append('Bridge')

    #Will it have outtro?
    if have_outtro:
        #It has an outtro
        #What outtro? Beat drop or guitar solo?
        outtro_style = choice(['BD', 'Solo'])
        song_structure.append(['Outtro', outtro_style])
    
    return song_structure
    

rola = Rola()
rolon = []
print(Rola())
for i in rola:
    if i == 'Intro':
        rolon.append(Intro())
    else:
        print('No Intro')

for r in rolon:
    for r1 in r[0]:
        print(r1)
    print(len(r[0]))


def play_snare(notas = []):
    for n in notas:
        for d in range(len(n)):
            if d % 2 == 0:
                drum.play_note(38, 0.33, n[d])
            else: 
                if d == 0.25:
                    drum.play_note(38, 0.33, n[d])
                else:
                    drum.play_note(38, 0, n[d])
                #drum.play_note(38, 0, n[d])

def play_bass_drum(notas = []):
    for n in notas:
        for d in range(len(n)):
            #if d % 2 != 0:
            drum.play_note(36, 0.33, n[d])
            #else:
                #drum.play_note(36, 0, n[d])

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



s.fork(play_hhat, args=[rolon[0][1]]) 
s.fork(play_snare, args=[rolon[0][0]])
s.fork(play_bass_drum, args=[rolon[0][0]])

s.wait_for_children_to_finish()