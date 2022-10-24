from random import seed
from abjad import Guitar
from scamp import *
import numpy as np
import time


s = Session()

s.tempo = 100

drum = s.new_midi_part('drums', 1)

def play_hat():
    for _ in range(16):
        drum.play_note(42, 1.0, 0.5)


def play_backbeat():
    for i in range(8):
        if i % 2 == 0:
            drum.play_note(36, 1.0, 1.0)
        else:
            drum.play_note(38, 1.0, 1.0)

fork(play_hat)
fork(play_backbeat)
wait_for_children_to_finish()