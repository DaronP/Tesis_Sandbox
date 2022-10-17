from random import random, seed, choice
from scamp import *
import random
import time
from instruments import *
from presets import *
import json

seed = 4875434493137809954

s_f = open('string.json')
p_f = open('percussion.json')

string = json.load(s_f)
rythm = json.load(p_f)


print(string['guitar_notes'][0])


s.fork(play_guitar, args=[string['guitar_notes'], string['g_rythm']])
s.fork(play_bass, args=[string['bass'], string['b_rythm']])
s.fork(play_kick_drum, args=[rythm['kick']])
s.fork(play_hhat, args=[rythm['hhat']]) 
s.fork(play_snare, args=[rythm['snare']])
s.fork(play_cimbal, args=[rythm['cimbal']])


s.wait_for_children_to_finish()