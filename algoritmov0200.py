from random import random, seed
from scamp import *
import random
from random import choice
import time
from instruments import *
from presets import *

s = Session()

s.tempo = 240

'''d_guitar = s.new_part('Distortion Guitar')
p_bass = s.new_part('Electric Bass (pick)')'''
drum = s.new_midi_part('drums', 1)


s.fork(play_kick_drum, args=[rythm_presets['kick-snare intermitent']['kick']])
s.fork(play_hhat, args=[rythm_presets['kick-snare intermitent']['hhat']]) 
s.fork(play_snare, args=[rythm_presets['kick-snare intermitent']['snare']])
s.fork(play_cimbal, args=[rythm_presets['kick-snare intermitent']['cimbal']])
s.wait_for_children_to_finish()