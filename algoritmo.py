from random import random, seed, choice
from scamp import *
import random
import time
from instruments import *
from presets import *

aeolian = [2, 1, 2, 2, 1, 2, 2]
mixolydian = [2, 2, 1, 2, 2, 1, 2]
blues_menor = [3, 2, 1, 1, 3, 2]
blues_mayor = [2, 1, 1, 3, 2, 3]
natural_mayor = [2, 2, 1, 2, 2, 2, 1]

chords_form = [2, 4]

d_file = open('Drum Map.txt', 'r')
drum_kit = d_file.readlines()




for i in range(len(drum_kit)):
    percussion = drum_kit[i]
    percussion = percussion.replace('\n', '')
    percussion = percussion.split(' - ')
    percussion[0] = int(percussion[0])
    drum_kit[i] = percussion
    #print(drum_kit[i])

def make_chords(pitch_f, flag=False):
    chords = []
    chords.append(pitch_f)
    if not flag:
        for i in chords_form:
            pitch_sum = pitch_f + sum(aeolian[:i])         
            chords.append(pitch_sum)
    else:
        mix = aeolian[1:]
        for i in chords_form:
            pitch_sum = pitch_f + sum(mix[:i])         
            chords.append(pitch_sum)
    
    return chords



def string_notes(pitch = 0):
    notes = [] 
    pila = []
    pila.append(pitch)
    for _ in range(0, 11):
        if not pila:
            pila.append(notes[-1][-1] + blues_menor[-1])
        for s in range(len(blues_menor) - 1):
            note = pila[-1] + blues_menor[s]
            if note <= 127:
                pila.append(note)
        notes.append(pila)
        pila = []
    
    for i in notes:
        print(i)

    return notes




'''scale_blues_m = string_notes()

for i in scale_blues_m:
    for j in i:
        play_bass(j)
        wait(1)
    print('octava')'''






#----------------------------------------------------------------------------------------------------------------
fund = list()

def Fundamental(mood='', part=''):

    kick_penta = []
    snare_penta = []
    hh_penta = []
    cimbal_penta = []

    figure = 5

    if part == 'chorus':
        figure -= 1
    if mood == 'melancholic':
        figure -= 2

    for i in range(1):
        for i in range(4):
            if i == 2:
                kick_penta.append(kick_penta[-i])
            elif i == 3:
                new_compas = []
                com_sum = 0
                for c in kick_penta[-2]:
                    com_sum += c
                    
                    if com_sum >= 3.0:
                        new_compas.append(c/2)
                        new_compas.append(c/2)
                    else:
                        new_compas.append(c)
                kick_penta.append(new_compas)
                    
            else:
                compas = []
                sum_compas = 0
                for j in range(4):
                    
                    sum_compas = sum(compas)
                    nota = 1/pow(2, random.randrange(2, figure))
                    nota = nota/0.25

                    if nota == 1.0:
                        compas.append(nota)

                    if nota == 0.5:
                        compas.append(nota)
                        compas.append(nota)
                        j += 1
                    if nota == 0.25:
                        compas.append(nota)
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
                        compas.append(nota)
                        j += 1
                    
                    if sum_compas >= 4.0:
                        i += 1
                        break
                
                kick_penta.append(compas)
        repetition = random.randrange(1, 4)
        for _ in range(repetition):
            for p in kick_penta[-4:]:
                kick_penta.append(p)


    fundamental = kick_penta.copy()

    snare_beats = bool(random.getrandbits(1))
    if snare_beats:
        print('3 SNAAAAAAAREZZZZZZ')
    else:
        print('2 - 4 SNAAAAAARAAAREZZZZZZZZZ')

    for i in range(len(kick_penta)):
        hh_compas = []
        snare_compas = []
        cimbal_compas = []
        for j in range(4):
            hh_compas.append(1.0)
            cimbal_compas.append(-1.0)
            if not snare_beats:
                if j == 1 or j == 3:
                    snare_compas.append(1.0)
                    kick_penta[i][j] *= -1
                else:
                    snare_compas.append(-1)
            else:
                if j == 2:
                    snare_compas.append(1.0)
                    kick_penta[i][j] *= -1
                else:
                    snare_compas.append(-1)

                    
        hh_penta.append(hh_compas)
        snare_penta.append(snare_compas)
        cimbal_penta.append(cimbal_compas)

    fundamental_rythm = {'fundamental': fundamental, 
                   'perc': {'kick': kick_penta, 
                            'hhat': hh_penta,
                            'snare': snare_penta,
                            'cimbal': cimbal_penta}}
    return fundamental_rythm

def Intro(fundamental):
    intro = {'guitar': [], 'kick': [], 'hhat': [], 'snare': [], 'cimbal': []}
    kick_penta = []
    snare_penta = []
    hh_penta = []
    cimbal_penta = []
    
    intro_desicion = random.choice(['Fundamental', 'Bridges'])

    kick = fundamental['kick'].copy()
    intro_kick=list()

    for compas in kick:
        pila = []
        pila_check = compas.copy()
        for note in range(len(compas)):
            try:
                if compas[note] == 1.0:
                    pila.append(compas[note])
                    pila_check[note] = 'done'
                else:
                    if pila_check[note] == 'done':
                        pass
                    elif compas[note] == compas[note + 1]:                            
                        pila.append(compas[note] * 2)
                        pila_check[note] = 'done'
                        pila_check[note + 1] = 'done'
                    elif (compas[note] * -1) == compas[note + 1]:
                        pila.append(compas[note] * (-2))
                        pila_check[note] = 'done'
                        pila_check[note + 1] = 'done'
                    else:
                        pila.append(compas[note])
                        pila_check[note] = 'done'
            except:
                pass
    
        intro_kick.append(pila)

    
    if intro_desicion == 'Fundamental':
        kick_penta = intro_kick
        hh_penta = fundamental['hhat'].copy()
        cimbal_penta = fundamental['cimbal'].copy()

        for i in range(len(kick_penta)):
            pila_snare = []
            for j in range(len(kick_penta[i])):
                pila_snare.append(kick_penta[i][j] * -1)
            snare_penta.append(pila_snare)
        
        intro['kick'] = kick_penta
        intro['snare'] = snare_penta
        intro['hhat'] = hh_penta
        intro['cimbal'] = cimbal_penta
        intro['guitar'] = kick_penta
        
        return intro

    elif intro_desicion == 'Bridges': #/*/*/*/*/*/*/*/*/*/*/*/*/*/**/
        intro['guitar'] = intro_kick



def Verse_desicion():
    desicions = set()
    presets_len = len(rythm_presets)
    for i in range(0, 4):
        n = random.randint(0, presets_len)
        if n == 4 and len(desicions) < 1:
            n = random.randint(0, (presets_len) - 1)

        desicions.add(n)

        if n == 2 and len(desicions) > 2:
            desicions.add(n)
            i += 1
        
        
    
    verse = []
    for _ in range(8):
        d = bool(random.getrandbits(1))
        if d:
            n = random.choice(list(desicions))

            verse.append(n)

            if verse[0] != n and 0 not in verse:
                verse.append(0)
        else:
            verse.append(0)
        
    if 0 not in verse:
        verse.insert(2, 0)
        verse.append(0)

    return verse

def Verso(riffs = {}):
    verso = {'guitar': [], 'kick': [], 'hhat': [], 'snare': [], 'cimbal': []}
    kick = []
    snare = []
    hhat = []
    cimbal = []
    guitar = []

    desicions = Verse_desicion()
    desicions_copy = desicions.copy()

    repetition = random.uniform(0, 1)
    print('rep = ', repetition)

    #Repeticion sencilla
    if repetition <= 0.33:
        for i in desicions_copy:
            desicions.append(i)
    elif repetition > 0.33 and repetition <= 0.66:
        for i in reversed(desicions_copy):
            desicions.append(i)

    for i in desicions:
        if i == 0:
            for r in riffs:
                for m in riffs[r]:
                    if r == 'kick':
                        kick.append(m)
                        guitar.append(m)
                    elif r == 'hhat':
                        hhat.append(m)
                    elif r == 'snare':
                        snare.append(m)
                    elif r == 'cimbal':
                        cimbal.append(m)
        else:
            for tech_num, (tech, perc) in enumerate(rythm_presets.items()):
                if i == tech_num + 1:                    
                    for instrument in perc:
                        for c in perc[instrument]:
                            if instrument == 'kick':
                                kick.append(c)
                                guitar.append(c)
                            elif instrument == 'snare':
                                snare.append(c)
                            elif instrument == 'hhat':
                                hhat.append(c)
                            elif instrument == 'cimbal':
                                cimbal.append(c)
    
    
    verso['kick'] = kick
    verso['hhat'] = hhat
    verso['snare'] = snare
    verso['cimbal'] = cimbal
    verso['guitar'] = guitar

    print(desicions)

    return verso



def Coro(fundamental):
    coro = {'guitar': [], 'kick': [], 'hhat': [], 'snare': [], 'cimbal': []}
    kick_penta = []
    snare_penta = []
    hh_penta = []
    cimbal_penta = []

    chorus_choise = random.choice(['New', 'Fundamental', 'Melodic'])
    print(chorus_choise, ' chorus')
    chorus_choise = 'New'
    
    if chorus_choise == 'New':
        chorus_rythm = Fundamental(part='chorus')['perc']
        coro['guitar'] = chorus_rythm['kick']
        coro['kick'] = chorus_rythm['kick']
        coro['snare'] = chorus_rythm['snare']
        coro['hhat'] = chorus_rythm['hhat']
        coro['cimbal'] = chorus_rythm['cimbal']

        return coro
    
    elif chorus_choise == 'Melodic':
        kick = fundamental['kick'].copy()
        chorus_guitar=list()

        for compas in kick:
            pila = []
            pila_check = compas.copy()
            for note in range(len(compas)):
                try:
                    if compas[note] == 1.0:
                        pila.append(compas[note])
                        pila_check[note] = 'done'
                    else:
                        if pila_check[note] == 'done':
                            pass
                        elif compas[note] == compas[note + 1]:                            
                            pila.append(compas[note] * 2)
                            pila_check[note] = 'done'
                            pila_check[note + 1] = 'done'
                        elif (compas[note] * -1) == compas[note + 1]:
                            pila.append(compas[note] * (-2))
                            pila_check[note] = 'done'
                            pila_check[note + 1] = 'done'
                        else:
                            pila.append(compas[note])
                            pila_check[note] = 'done'
                except:
                    pass
        
            chorus_guitar.append(pila)

        

        kick_penta = chorus_guitar
        hh_penta = fundamental['hhat'].copy()
        cimbal_penta = fundamental['cimbal'].copy()


        for i in range(len(kick_penta)):
            pila_snare = []
            for j in range(len(kick_penta[i])):
                pila_snare.append(kick_penta[i][j] * -1)
            snare_penta.append(pila_snare)
        
        coro['kick'] = kick_penta
        coro['snare'] = snare_penta
        coro['hhat'] = hh_penta
        coro['cimbal'] = cimbal_penta
        coro['guitar'] = kick_penta
        
        return coro

    elif chorus_choise == 'Fundamental':
        kick = fundamental['kick'].copy()
        chorus_guitar=list()

        for compas in kick:
            pila = []
            pila_check = compas.copy()
            for note in range(len(compas)):
                try:
                    if compas[note] == 1.0:
                        pila.append(compas[note])
                        pila_check[note] = 'done'
                    else:
                        if pila_check[note] == 'done':
                            pass
                        elif compas[note] == compas[note + 1]:                            
                            pila.append(compas[note] * 2)
                            pila_check[note] = 'done'
                            pila_check[note + 1] = 'done'
                        elif (compas[note] * -1) == compas[note + 1]:
                            pila.append(compas[note] * (-2))
                            pila_check[note] = 'done'
                            pila_check[note + 1] = 'done'
                        else:
                            pila.append(compas[note])
                            pila_check[note] = 'done'
                except:
                    pass
        
            chorus_guitar.append(pila)

        

        kick_penta = fundamental['kick'].copy()
        hh_penta = fundamental['hhat'].copy()
        cimbal_penta = fundamental['cimbal'].copy()
        snare_penta = fundamental['snare'].copy()
        
        coro['kick'] = kick_penta
        coro['snare'] = snare_penta
        coro['hhat'] = hh_penta
        coro['cimbal'] = cimbal_penta
        coro['guitar'] = chorus_guitar
        
        return coro




def Outtro():
    pass


def Rola():
    #Tendra intro?
    have_intro = 1#random.getrandbits(1)
    have_outtro = random.getrandbits(1)
    song_structure = []
    
    if have_intro == 1:
        song_structure.append('Intro')
    
    #Generic song structure
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
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////
rola = Rola()
rolon = dict()
verso1 = dict()
print(Rola())

rolon = Fundamental()
verso1 = Verso(rolon['perc'])
coro = Coro(rolon['perc'])

for i in rolon['fundamental']:
    print(i)
print(len(rolon['fundamental']))
print(len(verso1['kick']))
print(len(coro['kick']))
print('holi')


s.fork(play_kick_drum, args=[verso1['kick']])
s.fork(play_hhat, args=[verso1['hhat']]) 
s.fork(play_snare, args=[verso1['snare']])
s.fork(play_cimbal, args=[verso1['cimbal']])


s.wait_for_children_to_finish()