from random import random, seed, choice
from scamp import *
import random
import time
from instruments import *
from presets import *

scales = {'minor scales':{'aeolian': [2, 1, 2, 2, 1, 2, 2],      
                        'blues_minor': [3, 2, 1, 1, 3, 2],
                        'dorian': [2, 1, 2, 2, 2, 1, 2]},

          'major scales':{'mixolydian': [2, 2, 1, 2, 2, 1, 2],
                        'blues_major': [2, 1, 1, 3, 2, 3],
                        'natural_major': [2, 2, 1, 2, 2, 2, 1]}
        }

chords_form = [0, 2, 4]
tonalities = {'non-blues': [[0, 5, 3, 4], 
                            [5]],
              'blues': [[0, 4],
                        [0, 3, 4]
            ]}
scale = []
scale_name = ''
scale_chords = []
progression = []
f_pitch = 0



mood = 'aggressive'

d_file = open('Drum Map.txt', 'r')
drum_kit = d_file.readlines()


######################################-----------------------------------############################################

'''for i in range(len(drum_kit)):
    percussion = drum_kit[i]
    percussion = percussion.replace('\n', '')
    percussion = percussion.split(' - ')
    percussion[0] = int(percussion[0])
    drum_kit[i] = percussion
    #print(drum_kit[i])'''


def make_chords(scale=[], scale_form = 0):
    chords = []
    chords_pila = []
    count = 0
    for s in range(len(scale)):
        if count >= (scale_form - 1):
            chords.append(chords_pila)
            chords_pila = []
            count = 0
        else:
            try:
                pila = []
                for c in chords_form:
                    pila.append(scale[s + c])
                chords_pila.append(pila)
                count += 1
            except:
                pass
        
    return chords



def string_notes(pitch = 4, scale_name=''):
    notes = [] 
    pila = []
    pila.append(pitch)

    scale = []
    scale_name = ''

    if mood == 'aggressive' or mood == 'melancholic' and scale_name == '':
        scale_name = random.choice(list(scales['minor scales'].keys()))
        scale = scales['minor scales'][scale_name]
    elif mood == 'epic' and scale_name == '':
        scale_name = random.choice(list(scales['minor scales'].keys()))
        scale = scales['major scales'][scale_name]
    elif scale_name != '':
        try:
            scale = scales['minor scales'][scale_name]
        except:
            scale = scales['major scales'][scale_name]


    for _ in range(0, 11):
        if not pila:
            pila.append(notes[-1][-1] + scale[-1])
        for s in range(len(scale) - 1):
            note = pila[-1] + scale[s]
            if note <= 127:
                pila.append(note)
        notes.append(pila)
        pila = []
    
    for i in notes:
        print(i)
    
    flat_str_notes = [item for sublist in notes for item in sublist]
    scale_chords = make_chords(scale=flat_str_notes, scale_form = len(notes[0]))

    for i in scale_chords:
        print(i)

    return [notes, scale_name, scale_chords]



def make_progression(scale_name):
    progresion = []
    tonality = []

    if 'blues' in scale_name:
        tonality = random.choice(tonalities['blues'])
    else:
        blues = random.choice(list(tonalities.keys()))
        tonality = random.choice(tonalities[blues])

    print(tonality, len(tonality))
    
    for i in range(8):
        if len(tonality) == 1:
            for i in range(8):
                progresion.append(0)
            return progresion

        if i == 0:
            progresion.append(tonality[0])
        elif i > 0 and i <= 3:
            prob = random.uniform(0, 1)
            if prob >= 0.5:
                progresion.append(tonality[0])
            else:
                tonal = random.choice(tonality[-(len(tonality) - 2):])
                progresion.append(tonal)
        elif i >= 4:
            tonal = random.choice(tonality)
            progresion.append(tonal)
        
    if progresion[-1] != 0:
        progresion[-1] = 0

    print(progresion)
    return progresion

def make_bass(rythm):
    bass_compas = []

    p_count = 0
    for r in range(8):
        bass_pila = []
        
        for n in rythm[r]:
            if p_count != 4 and p_count != 8 and p_count != 3 and p_count != 7:
                bass_pila.append(scale_chords[2][progression[p_count]][0])
            elif p_count == 4 or p_count == 8:
                prob = random.uniform(0, 1)
                if prob >= 0.5:
                    bass_pila.append(scale_chords[2][progression[p_count]][-1])
                else:
                    bass_pila.append(scale_chords[2][progression[p_count]][0])
            elif p_count == 3 or p_count == 7:
                prob = random.uniform(0, 1)
                if prob >= 0.25:
                    bass_pila.append(scale_chords[2][progression[p_count]][-2])
                else:
                    bass_pila.append(scale_chords[2][progression[p_count]][0])

        bass_compas.append(bass_pila)
        bass_pila = []
        p_count += 1
        if p_count >= len(progression):
            p_count = 0
    
    for _ in range(int(len(rythm)/8)):
        for j in range(8):
            bass_compas.append(bass_compas[j])

    return bass_compas

def make_guitar(rythm):
    guitar_compas = []

    p_count = 0
    for r in range(8):
        guitar_pila = []
        random_octave = random.randint(4, 6)
        arp_count = 0
        
        for n in rythm[r]:
            if n == 1.0 or n == 0.5:
                if mood == 'aggressive':
                    guitar_pila.append([scale_chords[3][progression[p_count]][0], scale_chords[3][progression[p_count]][-1]])
                    arp_count = 0

            else:                
                guitar_pila.append(scale_chords[random_octave][progression[p_count]][arp_count])
                arp_count += 1
                if arp_count > 2: 
                    arp_count = 0

        guitar_compas.append(guitar_pila)
        guitar_pila = []
        p_count += 1

        if p_count >= len(progression):
            p_count = 0
    
    for _ in range(int(len(rythm)/8)):
        for j in range(8):
            guitar_compas.append(guitar_compas[j])

    return guitar_compas






######################################-----------------------------------############################################

def Fundamental(part=''):

    kick_penta = []
    snare_penta = []
    hh_penta = []
    cimbal_penta = []
    guitar = []

    figure = 5

    #Chechinkg part of song to discard 1/32 notes
    if part == 'chorus':
        figure -= 1

    #Checking mood to discard 1/16 and 1/32 notes
    if mood == 'melancholic':
        figure -= 2

    #Building fundamental rythm
    for _ in range(1):
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
                    
                    #Black notes
                    if nota == 1.0:
                        compas.append(nota)

                    #1/8 notes
                    if nota == 0.5:
                        compas.append(nota)
                        compas.append(nota)
                        j += 1
                    #1/16 notes
                    if nota == 0.25:
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        j += 1
                    #1/32 notes
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
                    
                    #Breaking if 4/4
                    if sum_compas >= 4.0:
                        i += 1
                        break
                
                kick_penta.append(compas)
        
        #Repeating for 8 bars
        for p in kick_penta[-4:]:
            kick_penta.append(p)


    fundamental = kick_penta.copy()

    #Choice of snare: 0 for snare in 2 and 4, 1 for snare in 3
    snare_beats = bool(random.getrandbits(1))

    #Building hi-hat, snare and silenced cimbal
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

        #Appending instruments
        hh_penta.append(hh_compas)
        snare_penta.append(snare_compas)
        cimbal_penta.append(cimbal_compas)

    for i in range(len(kick_penta)):
        guitar.append(kick_penta[i])    


    fundamental_rythm = {'string': {'guitar': guitar}, 
                   'perc': {'kick': kick_penta, 
                            'hhat': hh_penta,
                            'snare': snare_penta,
                            'cimbal': cimbal_penta}}
    return fundamental_rythm

def reduce_notes(rythm):
    reduced = []
    for compas in rythm:
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
        reduced.append(pila)
    
    return reduced

def Intro(strings, fundamental):
    intro = {'guitar': [], 'kick': [], 'hhat': [], 'snare': [], 'cimbal': []}
    kick_penta = []
    snare_penta = []
    hh_penta = []
    cimbal_penta = []
    
    intro_desicion = random.choice(['Fundamental', 'Ambience'])

    kick = fundamental['kick'].copy()
    intro_kick = reduce_notes(strings)

    
    if intro_desicion == 'Fundamental':
        guitar_penta = intro_kick
        kick_penta = fundamental['kick'].copy()
        hh_penta = fundamental['hhat'].copy()
        snare_penta = fundamental['snare'].copy()
        cimbal_penta = fundamental['cimbal'].copy()

        '''for i in range(len(kick_penta)):
            pila_snare = []
            for j in range(len(kick_penta[i])):
                pila_snare.append(kick_penta[i][j] * -1)
            snare_penta.append(pila_snare)'''
        
        intro['kick'] = kick_penta
        intro['snare'] = snare_penta
        intro['hhat'] = hh_penta
        intro['cimbal'] = cimbal_penta
        intro['guitar'] = guitar_penta
        
        return intro
    
    if intro_desicion == 'Ambience':
        reduced = []
        for compas in intro_kick:
            pila = []
            pila_check = compas.copy()
            for note in range(len(compas)):
                try:
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
                    pila.append(compas[note])
                    pila_check[note] = 'done'
            reduced.append(pila)

        for i in range(8):
            k_pila = []
            s_pila = []
            h_pila = []
            c_pila = []

            for _ in range(4):
                k_pila.append(-1.0)
                h_pila.append(-1.0)
                s_pila.append(-1.0)
                c_pila.append(-1.0)
            
            kick_penta.append(k_pila)
            snare_penta.append(s_pila)
            hh_penta.append(h_pila)
            cimbal_penta.append(c_pila)

        
        intro['kick'] = kick_penta
        intro['snare'] = snare_penta
        intro['hhat'] = hh_penta
        intro['cimbal'] = cimbal_penta
        intro['guitar'] = reduced

        return intro







def Verse_desicion():
    desicions = set()
    presets_len = len(rythm_presets) - 1
    for i in range(0, 4):
        n = random.randint(0, presets_len)
        if n == 4 and len(desicions) < 1:
            n = random.randint(0, (presets_len) - 1)

        desicions.add(n)

        if n == 2 and len(desicions) > 2:
            desicions.add(n)
            i += 1        
    
    verse = []

    verse_limit = random.choice([4, 8])
    
    while len(verse) < verse_limit:
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

def Verso(string, rythm):
    verso = {'guitar': [], 'kick': [], 'hhat': [], 'snare': [], 'cimbal': [], 'leads': [], 'bass_notes': []}
    kick = []
    snare = []
    hhat = []
    cimbal = []
    guitar = []
    leads = []
    bass = []

    #Desicions for verse rythm
    desicions = Verse_desicion()
    desicions_copy = desicions.copy()

    #Deciding rythm change for aggressive mood
    rythm_change = bool(random.getrandbits(1))

    if rythm_change and mood == 'aggressive':
        rythm_steady = bool(random.getrandbits(1))
        if not rythm_steady:
            string[1] = string[0]
            string[5] = string[0]
        else:
            string[1] = string[0]
            string[3] = string[0]
            string[5] = string[0]
    
    #Checking for leads
    for d in range(len(desicions)):
        try:
            if desicions[d] == 0 and desicions[d] == desicions[d + 1] and desicions[d + 1] == desicions[d + 2] and desicions[d + 2] == desicions[d + 3]:
                leads_bool = True
        except:
            pass
    
    leads_bool = True


    #Reprtition
    repetition = 1

    #Sin repeticion
    if len(desicions) > 4:
        pass
    else: #Repeticion
        repetition = random.uniform(0, 1)
        print('rep = ', repetition)
        #Repeticion sencilla
        if repetition <= 0.33:
            for i in desicions_copy:
                desicions.append(i)
        #Repeticion en reversa
        elif repetition > 0.33 and repetition <= 0.66:
            for i in reversed(desicions_copy):
                desicions.append(i)
        #repeticion > 0.66 no hay repeticion
    
    
    #Building verse rythm
    for i in desicions: 
        for s in string:
            guitar.append(s)

        if i == 0: #If fundamental rythm
            for r in rythm:
                for m in rythm[r]:
                    if r == 'kick':
                        kick.append(m)
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
                            elif instrument == 'snare':
                                snare.append(c)
                            elif instrument == 'hhat':
                                hhat.append(c)
                            elif instrument == 'cimbal':
                                cimbal.append(c)
            
        

    #Checking verse length to be multiple of 8 between 32 and 48 bars
    if len(kick) % 8 == 0 and len(kick) > 32 and len(kick) <= 48:
        pass
    elif len(kick) > 32:
        print(len(kick))
        while len(kick) % 8 != 0 and len(kick) >= 48:
            del kick[-1]
            del guitar[-1]
            del snare[-1]
            del hhat[-1]
            del cimbal[-1]
    elif len(kick) < 28:
        while len(kick) < 32:
            kick.append(kick[-1])
            guitar.append(guitar[-1])
            snare.append(snare[-1])
            hhat.append(hhat[-1])
            cimbal.append(cimbal[-1])
    
    #Checking for same bar lengths between guitar and the rest
    while len(guitar) > len(kick):
        del guitar[-1]

    if leads_bool:
        for k in kick:
            leads_pila = []
            for _ in range(16):
                silence_prob = random.uniform(0, 1)
                if silence_prob <= 0.25:
                    leads_pila.append(-0.25)
                else:
                    leads_pila.append(0.25)
            leads.append(leads_pila)

    
    #Getting bass
    bass = make_bass(rythm=guitar)

    guitar_notes = make_guitar(rythm=guitar)

    play_bass(notas=bass, rythm=guitar)

    
    verso['kick'] = kick
    verso['hhat'] = hhat
    verso['snare'] = snare
    verso['cimbal'] = cimbal
    verso['guitar'] = guitar
    verso['leads'] = leads
    verso['bass_notes'] = bass
    verso['guitar_notes'] = guitar_notes

    print(desicions)

    return verso



def Coro(string, fundamental):
    coro = {'guitar': [], 'kick': [], 'hhat': [], 'snare': [], 'cimbal': []}
    kick_penta = []
    snare_penta = []
    hh_penta = []
    cimbal_penta = []

    chorus_choise = random.choice(['New', 'Fundamental', 'Melodic'])
    print(chorus_choise, ' chorus')

    repetition = random.randint(3,6)
    
    if chorus_choise == 'New':
        new_fundamental = Fundamental(part='chorus')
        chorus_rythm = new_fundamental['perc']
        chorus_string = reduce_notes(new_fundamental['string']['guitar'])

        for _ in range(repetition):
            for i in range(len(chorus_rythm['kick'])):
                coro['guitar'].append(chorus_string[i])
                coro['kick'].append(chorus_rythm['kick'][i])
                coro['snare'].append(chorus_rythm['snare'][i])
                coro['hhat'].append(chorus_rythm['hhat'][i])
                coro['cimbal'].append(chorus_rythm['cimbal'][i])
        
        return coro
    
    elif chorus_choise == 'Melodic':
        kick = fundamental['kick'].copy()

        chorus_guitar = reduce_notes(kick)

        kick_penta = chorus_guitar
        hh_penta = fundamental['hhat'].copy()
        snare_penta = fundamental['snare'].copy()
        cimbal_penta = fundamental['cimbal'].copy()


        '''for i in range(len(kick_penta)):
            pila_snare = []
            for j in range(len(kick_penta[i])):
                pila_snare.append(kick_penta[i][j] * -1)
            snare_penta.append(pila_snare)'''
        
        for _ in range(repetition):
            for k in range(len(kick_penta)):
                coro['kick'].append(kick_penta[k])
                coro['snare'].append(snare_penta[k])
                coro['hhat'].append(hh_penta[k])
                coro['cimbal'].append(cimbal_penta[k])
                coro['guitar'].append(chorus_guitar[k])
        
        return coro

    elif chorus_choise == 'Fundamental':
        kick = fundamental['kick'].copy()

        chorus_guitar = reduce_notes(kick)        

        kick_penta = fundamental['kick'].copy()
        hh_penta = fundamental['hhat'].copy()
        cimbal_penta = fundamental['cimbal'].copy()
        snare_penta = fundamental['snare'].copy()
        
        for _ in range(repetition):
            for k in range(len(kick_penta)):
                coro['kick'].append(kick_penta[k])
                coro['snare'].append(snare_penta[k])
                coro['hhat'].append(hh_penta[k])
                coro['cimbal'].append(cimbal_penta[k])
                coro['guitar'].append(chorus_guitar[k])
        
        return coro




def Outtro():
    pass


def Composer():
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
composer = Composer()
composition = dict()
verso1 = dict()
print(Composer())

#Getting scale and chords
scale, scale_name, scale_chords = string_notes(pitch=9)

#Getting chords progression
progression = make_progression(scale_name)

composition = Fundamental()

Intro(composition['string']['guitar'], composition['perc'])
verso1 = Verso(composition['string']['guitar'], composition['perc'])
coro = Coro(composition['string']['guitar'], composition['perc'])

for i in composition['string']['guitar']:
    print(i)
print(len(composition['string']), ' len of fundamental')
print('length of verse: ', (len(verso1['kick'])*4)/(s.tempo/60))
print('length of chorus: ', (len(coro['kick'])*4)/(s.tempo/60))
print('holi')


'''s.fork(play_kick_drum, args=[verso1['kick']])
s.fork(play_hhat, args=[verso1['hhat']]) 
s.fork(play_snare, args=[verso1['snare']])
s.fork(play_cimbal, args=[verso1['cimbal']])'''

s.fork(play_kick_drum, args=[coro['kick']])
s.fork(play_hhat, args=[coro['hhat']]) 
s.fork(play_snare, args=[coro['snare']])
s.fork(play_cimbal, args=[coro['cimbal']])


s.wait_for_children_to_finish()