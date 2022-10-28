from random import random
from scamp import *
import random
import time
from presets import *
import json
import sys



class Algorithm:

    def __init__(self):

        self.seed = 0

        self.scales = {'minor scales':{'aeolian': [2, 1, 2, 2, 1, 2, 2],      
                                'blues_minor': [3, 2, 1, 1, 3, 2],
                                'dorian': [2, 1, 2, 2, 2, 1, 2]},

                'major scales':{'mixolydian': [2, 2, 1, 2, 2, 1, 2],
                                'blues_major': [2, 1, 1, 3, 2, 3],
                                'natural_major': [2, 2, 1, 2, 2, 2, 1]}
                }

        self.chords_form = [0, 2, 4]
        self.tonalities = {'non-blues': [[0, 5, 3, 4], 
                                    [5]],
                    'blues': [[0, 4],
                                [0, 3, 4]
                    ]}
        self.scale = []
        self.scale_name = ''
        self.scale_chords = []
        self.progression = []
        self.pitch = 0

        self.moods = ['aggressive', 'epic', 'melancholic']
        self.mood = ''


    ######################################-----------------------------------############################################


    def make_chords(self, scale=[], scale_form = 0):
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
                    for c in self.chords_form:
                        pila.append(scale[s + c])
                    chords_pila.append(pila)
                    count += 1
                except:
                    pass
            
        return chords



    def string_notes(self, pitch = 4, sname=''):
        notes = [] 
        pila = []
        pila.append(pitch)

        scale = []
        scale_name = sname

        if self.mood == 'aggressive' or self.mood == 'melancholic' and scale_name == '':
            scale_name = random.choice(list(self.scales['minor scales'].keys()))
            scale = self.scales['minor scales'][scale_name]
        elif self.mood == 'epic' and scale_name == '':
            scale_name = random.choice(list(self.scales['major scales'].keys()))
            scale = self.scales['major scales'][scale_name]
        elif scale_name != '':
            try:
                scale = self.scales['minor scales'][scale_name]
            except:
                scale = self.scales['major scales'][scale_name]


        for _ in range(0, 11):
            if not pila:
                pila.append(notes[-1][-1] + scale[-1])
            for s in range(len(scale) - 1):
                note = pila[-1] + scale[s]
                if note <= 127:
                    pila.append(note)
            notes.append(pila)
            pila = []

        
        flat_str_notes = [item for sublist in notes for item in sublist]
        scale_chords = self.make_chords(scale=flat_str_notes, scale_form = len(notes[0]))


        return [notes, scale_name, scale_chords]



    def make_progression(self, scale_name):
        progresion = []
        tonality = []

        if 'blues' in scale_name:
            tonality = random.choice(self.tonalities['blues'])
        else:
            blues = random.choice(list(self.tonalities.keys()))
            tonality = random.choice(self.tonalities[blues])
        
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

        return progresion

    def make_bass(self, rythm):
        bass_compas = []

        p_count = 0
        for r in range(len(rythm)):
            compas = []

            if p_count >= 7:
                p_count = 0

            for n in rythm[r]:
                if p_count == 3 or p_count == 7:
                    fifth = bool(random.getrandbits(1))
                    if fifth:
                        compas.append(self.scale_chords[2][self.progression[p_count]][-1])
                    else:
                        compas.append(self.scale_chords[2][self.progression[p_count]][0])
                elif p_count == 2 or p_count == 6:
                    compas.append(self.scale_chords[2][self.progression[p_count]][1])
                else:
                    compas.append(self.scale_chords[2][self.progression[p_count]][0])
            bass_compas.append(compas)
            p_count += 1


        return bass_compas

    def allEqual(self, iterable):
        iterator = iter(iterable)
        
        try:
            firstItem = next(iterator)
        except StopIteration:
            return True
            
        for x in iterator:
            if x!=firstItem:
                return False
        return True

    def make_guitar(self, rythm, isLeads=False, isChorus=False):
        guitar_notes = []
        prog_count = 0
        random_octave = 0

        if isLeads:
            random_octave = random.randint(4, 6)
        
        if not isChorus:
            for r in rythm:
                if prog_count >= 8:
                    prog_count = 0
                compas = []
                for i in range(len(r)):
                    if ((r[i] == 0.25 or r[i] == 0.125) and isLeads == False) or (self.allEqual(r) and r[i] == 0.5):
                        if self.mood == 'aggressive':
                            compas.append([self.scale_chords[2][0][0], self.scale_chords[2][0][-1]])
                        else:
                            random_octave = random.randint(2, 4)
                            compas.append([self.scale_chords[random_octave][self.progression[prog_count]][0], self.scale_chords[2][self.progression[prog_count]][-1]])
                    else:
                        if i == 0:
                            compas.append(self.scale_chords[2][self.progression[prog_count]][0])
                        else:
                            random_note = random.randint(0, 2)
                            if isLeads == False:
                                compas.append(self.scale_chords[3][self.progression[prog_count]][random_note])
                            else:
                                compas.append(self.scale_chords[random_octave][self.progression[prog_count]][random_note])
                guitar_notes.append(compas)
                prog_count += 1

        else:
            for r in rythm:
                if prog_count >= 8:
                    prog_count = 0
                compas = []
                for i in range(len(r)):
                    compas.append(self.scale_chords[4][self.progression[prog_count]])
                guitar_notes.append(compas)
                prog_count += 1


        return guitar_notes






    ######################################-----------------------------------############################################

    def Fundamental(self, part=''):

        kick_penta = []
        snare_penta = []
        hh_penta = []
        cimbal_penta = []
        guitar = []

        #Epic mood defaults
        blacks = 2
        figure = 4

        

        #Checking mood to discard 1/16 and 1/32 notes
        if self.mood == 'melancholic':
            blacks = 2
            figure = 4
        
        #Discarding 1/4 notes for aggressive
        if self.mood == 'aggressive':
            blacks = 2
            figure = 4
        
        #Chechinkg part of song to discard 1/32 notes
        if part == 'chorus':
            blacks = 2
            figure = 3

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
                        nota = 1/pow(2, random.randrange(blacks, figure))
                        nota = nota/0.25

                        #White notes
                        if nota == 2.0:
                            compas.append(nota)
                        
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
        
        #Rearanging bars so 1/16 and 1/32 are first to play in aggressive mood
        if self.mood == 'aggressive':
            for i in range(len(kick_penta)):
                for j in range(len(kick_penta[i])):
                    if (0.25 in kick_penta[i] or 0.125 in kick_penta[i]) and (j > len(kick_penta[i])/2):
                        kick_penta[i] = kick_penta[i][::-1]
                        break


        for i in range(len(kick_penta)):
            guitar.append(kick_penta[i].copy()) 

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
                        try:
                            kick_penta[i][j] *= -1
                        except:
                            pass
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
    

        #Reducing 1/32 for acentuation in kick
        for i in range(len(guitar)):
            for j in range(len(guitar[i])):
                try:
                    if guitar[i][j] == 0.125 and guitar[i][j] == guitar[i][j + 1]:
                        guitar[i][j] = 0.25 
                        del guitar[i][j + 1]
                except:
                    pass



        fundamental_rythm = {'string': {'guitar': guitar}, 
                    'perc': {'kick': kick_penta, 
                                'hhat': hh_penta,
                                'snare': snare_penta,
                                'cimbal': cimbal_penta}}


        return fundamental_rythm

    def reduce_notes(self, rythm):
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

    def Intro(self, strings, fundamental):
        intro = {'guitar': [], 'kick': [], 'hhat': [], 'snare': [], 'cimbal': [], 'guitar_notes': [], 'bass': [], 'bass_rythm': []}
        kick_penta = []
        snare_penta = []
        hh_penta = []
        cimbal_penta = []
        
        intro_desicion = random.choice(['Fundamental', 'Ambience'])

        kick = fundamental['kick'].copy()
        intro_kick = self.reduce_notes(strings)

        
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
            intro['bass_rythm'] = intro['guitar'].copy()

            guitar_notes = self.make_guitar(rythm=intro['guitar'])
            bass_notes = self.make_bass(intro['guitar'])

            intro['guitar_notes'] = guitar_notes
            intro['bass'] = bass_notes
            
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
            intro['bass_rythm'] = [[ -1 * i for i in inner ] for inner in intro['guitar']]

            guitar_notes = self.make_guitar(rythm=intro['guitar'])
            bass_notes = self.make_bass(intro['guitar'])

            intro['guitar_notes'] = guitar_notes
            intro['bass'] = bass_notes

            return intro



    def Verse_desicion(self):
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

    def Verso(self, string, rythm):
        verso = {'guitar': [], 'kick': [], 'hhat': [], 'snare': [], 'cimbal': [], 'leads': [], 'bass': [], 'bass_rythm': [], 'guitar_notes': []}
        kick = []
        snare = []
        hhat = []
        cimbal = []
        guitar = []
        leads = []
        bass = []

        #Desicions for verse rythm
        desicions = self.Verse_desicion()
        desicions_copy = desicions.copy()

        #Deciding rythm change (power chords) for aggressive mood
        rythm_change = bool(random.getrandbits(1))
        rythm_change = True

        if rythm_change and self.mood == 'aggressive':
            rythm_steady = bool(random.getrandbits(1))
            if not rythm_steady:
                string[0] = [0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25]
                string[1] = [0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25]
                string[4] = [0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25]
                string[5] = [0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25]

                rythm['kick'][0] = [0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25]
                rythm['kick'][1] = [0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25]
                rythm['kick'][4] = [0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25]
                rythm['kick'][5] = [0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25, 0.25, 0.25, 0.25, -0.25]
            else:
                string[0] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
                string[1] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
                string[2] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
                string[4] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

                rythm['kick'][0] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
                rythm['kick'][1] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
                rythm['kick'][2] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
                rythm['kick'][4] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        
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
                
            

        #Checking verse length to be multiple of 8 between 16 and 32 bars
        if len(kick) % 8 == 0 and len(kick) > 16 and len(kick) <= 32:
            pass
        elif len(kick) > 16:
            while len(kick) % 8 != 0 and len(kick) >= 32:
                del kick[-1]
                del guitar[-1]
                del snare[-1]
                del hhat[-1]
                del cimbal[-1]
        elif len(kick) < 16:
            while len(kick) < 32:
                kick.append(kick[-1])
                guitar.append(guitar[-1])
                snare.append(snare[-1])
                hhat.append(hhat[-1])
                cimbal.append(cimbal[-1])
        
        #Checking for same bar lengths between guitar and the rest
        while len(kick) > 32:
            del kick[-1]
            del snare[-1]
            del hhat[-1]
            del cimbal[-1]
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
        bass = self.make_bass(rythm=guitar)

        guitar_notes = self.make_guitar(rythm=guitar)    

        
        verso['kick'] = kick
        verso['hhat'] = hhat
        verso['snare'] = snare
        verso['cimbal'] = cimbal
        verso['guitar'] = guitar
        verso['leads'] = leads
        verso['bass'] = bass
        verso['guitar_notes'] = guitar_notes
        verso['bass_rythm'] = guitar.copy()

        return verso



    def Coro(self, fundamental):
        coro = {'guitar': [], 'kick': [], 'hhat': [], 'snare': [], 'cimbal': [], 'bass': [], 'guitar_notes': [], 'bass_rythm': []}
        kick_penta = []
        snare_penta = []
        hh_penta = []
        cimbal_penta = []

        chorus_choise = random.choice(['New', 'Fundamental', 'Melodic'])

        if self.mood == 'aggressive':
            repetition = random.randint(2,3)

        elif self.mood == 'epic' or self.mood == 'melancholic':
            repetition = random.randint(1,2)
        
        if chorus_choise == 'New':
            new_fundamental = self.Fundamental(part='chorus')
            chorus_rythm = new_fundamental['perc']
            chorus_string = []
            
            if self.mood == 'melancholic' or self.mood == 'epic':
                for _ in range(len(chorus_rythm['kick'])):
                    chorus_string.append([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
            else:
                chorus_string = new_fundamental['string']['guitar']

            for _ in range(repetition):
                for i in range(len(chorus_rythm['kick'])):
                    coro['guitar'].append(chorus_string[i])
                    coro['bass'].append(chorus_string[i])
                    coro['kick'].append(chorus_rythm['kick'][i])
                    coro['snare'].append(chorus_rythm['snare'][i])
                    coro['hhat'].append(chorus_rythm['hhat'][i])
                    coro['cimbal'].append(chorus_rythm['cimbal'][i])
            
            guitar_chords = self.make_guitar(coro['guitar'], isChorus=True)
            bass_notes = self.make_bass(coro['guitar'])

            coro['guitar_notes'] = guitar_chords
            coro['bass'] = bass_notes
            coro['bass_rythm'] = coro['guitar'].copy()

            
            return coro
        
        elif chorus_choise == 'Melodic':
            kick = fundamental['kick'].copy()

            chorus_guitar = []

            if self.mood == 'melancholic' or self.mood == 'epic':
                for _ in range(len(kick)):
                    chorus_guitar.append([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
            else:
                chorus_guitar = self.reduce_notes(fundamental['kick'])

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

            guitar_chords = self.make_guitar(coro['guitar'], isChorus=True)
            bass_notes = self.make_bass(coro['kick'])

            coro['guitar_notes'] = guitar_chords
            coro['bass'] = bass_notes
            coro['bass_rythm'] = coro['kick'].copy()
            
            return coro

        elif chorus_choise == 'Fundamental':
            kick = fundamental['kick'].copy()

            chorus_guitar = []

            if self.mood == 'melancholic' or self.mood == 'epic':
                for _ in range(len(kick)):
                    chorus_guitar.append([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])  
            else:
                chorus_guitar = self.reduce_notes(fundamental['kick'])    

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

            guitar_chords = self.make_guitar(coro['guitar'], isChorus=True)
            bass_notes = self.make_bass(coro['guitar'])

            coro['guitar_notes'] = guitar_chords
            coro['bass'] = bass_notes
            coro['bass_rythm'] = coro['guitar'].copy()
            
            return coro




    def Outro(self, verse, last_chord):
        outro = verse.copy()

        l = len(outro['kick'])

        new_l = int(l/2)

        for _ in range(new_l):
            del outro['guitar'][-1]
            del outro['guitar_notes'][-1]

            del outro['bass_rythm'][-1]
            del outro['bass'][-1]

            del outro['kick'][-1]
            del outro['snare'][-1]
            del outro['hhat'][-1]
            del outro['cimbal'][-1]
        
        outro['guitar'][0] = [4.0]
        outro['guitar_notes'][0] = [last_chord]
        outro['guitar'][1] = [-4.0]
        outro['guitar_notes'][1] = [last_chord]

        outro['bass_rythm'][0] = [-4.0]
        outro['bass'][0] = [last_chord[0]]
        outro['bass_rythm'][1] = [-4.0]
        outro['bass'][1] = [last_chord[0]]

        outro['kick'][0] = [-1.0, -1.0, -1.0, -1.0]
        outro['snare'][0] = [-1.0, -1.0, -1.0, -1.0]
        outro['hhat'][0] = [1.0, 1.0, 1.0, 1.0]
        outro['cimbal'][0] = [-1.0, -1.0, -1.0, -1.0]
        outro['kick'][1] = [-1.0, -1.0, -1.0, -1.0]
        outro['snare'][1] = [-1.0, -1.0, -1.0, -1.0]
        outro['hhat'][1] = [1.0, 1.0, 1.0, 1.0]
        outro['cimbal'][1] = [-1.0, -1.0, -1.0, -1.0]
        
        try:
            del outro['leads']
        except:
            pass

        return(outro)



    def Composer(self):
        #Tendra intro?
        have_intro = random.getrandbits(1)
        have_outtro = random.getrandbits(1)
        song_structure = []
        song_string_composed = {
                                'guitar_notes':[],
                                'bass':[],
                                'b_rythm':[],
                                'g_rythm': []
                                }
        song_rythm_composed = {
                                'kick': [], 
                                'hhat': [], 
                                'snare': [], 
                                'cimbal': []
                                }
        
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
            song_structure.append('Verse')
        else:
            #Same verse
            song_structure.append('S_Verse')

        song_structure.append('Chorus')

        #Will it have outtro?
        if have_outtro and self.mood == 'aggressive':
            #It has an outtro
            song_structure.append('Outro')
        
        composition = dict()
        verso1 = dict()

        composition = self.Fundamental()

        intro = {}
        verso1 = {}
        coro = {}
        verso2 = {}
        outro = {}

        for i in range(len(song_structure)):
            if song_structure[i] == 'Intro':
                intro = self.Intro(composition['string']['guitar'], composition['perc'])

                for c in range(len(intro['kick'])):
                    song_string_composed['guitar_notes'].append(intro['guitar_notes'][c])
                    song_string_composed['bass'].append(intro['bass'][c])
                    song_string_composed['g_rythm'].append(intro['guitar'][c])
                    song_string_composed['b_rythm'].append(intro['bass_rythm'][c])

                    song_rythm_composed['kick'].append(intro['kick'][c])
                    song_rythm_composed['snare'].append(intro['snare'][c])
                    song_rythm_composed['hhat'].append(intro['hhat'][c])
                    song_rythm_composed['cimbal'].append(intro['cimbal'][c])

            if song_structure[i] == 'Verse':
                verso1 = self.Verso(composition['string']['guitar'], composition['perc'])

                for c in range(len(verso1['kick'])):
                    song_string_composed['guitar_notes'].append(verso1['guitar_notes'][c])
                    song_string_composed['bass'].append(verso1['bass'][c])
                    song_string_composed['g_rythm'].append(verso1['guitar'][c])
                    song_string_composed['b_rythm'].append(verso1['bass_rythm'][c])

                    song_rythm_composed['kick'].append(verso1['kick'][c])
                    song_rythm_composed['snare'].append(verso1['snare'][c])
                    song_rythm_composed['hhat'].append(verso1['hhat'][c])
                    song_rythm_composed['cimbal'].append(verso1['cimbal'][c])
            
            if song_structure[i] == 'S_Verse':
                verso2 = verso1

                for c in range(len(verso2['kick'])):
                    song_string_composed['guitar_notes'].append(verso2['guitar_notes'][c])
                    song_string_composed['bass'].append(verso2['bass'][c])
                    song_string_composed['g_rythm'].append(verso2['guitar'][c])
                    song_string_composed['b_rythm'].append(verso2['bass_rythm'][c])

                    song_rythm_composed['kick'].append(verso2['kick'][c])
                    song_rythm_composed['snare'].append(verso2['snare'][c])
                    song_rythm_composed['hhat'].append(verso2['hhat'][c])
                    song_rythm_composed['cimbal'].append(verso2['cimbal'][c])

            if song_structure[i] == 'Chorus':
                coro = self.Coro(composition['perc'])

                for c in range(len(coro['kick'])):
                    song_string_composed['guitar_notes'].append(coro['guitar_notes'][c])
                    song_string_composed['bass'].append(coro['bass'][c])
                    song_string_composed['g_rythm'].append(coro['guitar'][c])
                    song_string_composed['b_rythm'].append(coro['bass_rythm'][c])

                    song_rythm_composed['kick'].append(coro['kick'][c])
                    song_rythm_composed['snare'].append(coro['snare'][c])
                    song_rythm_composed['hhat'].append(coro['hhat'][c])
                    song_rythm_composed['cimbal'].append(coro['cimbal'][c])

            if song_structure[i] == 'Outro':
                outro = self.Outro(verso1, song_string_composed['guitar_notes'][-1][-1])

                for c in range(len(outro['kick']) - 1):
                    song_string_composed['guitar_notes'].append(outro['guitar_notes'][c])
                    song_string_composed['bass'].append(outro['bass'][c])
                    song_string_composed['g_rythm'].append(outro['guitar'][c])
                    song_string_composed['b_rythm'].append(outro['bass_rythm'][c])

                    song_rythm_composed['kick'].append(outro['kick'][c])
                    song_rythm_composed['snare'].append(outro['snare'][c])
                    song_rythm_composed['hhat'].append(outro['hhat'][c])
                    song_rythm_composed['cimbal'].append(outro['cimbal'][c])

        song = {'string': song_string_composed, 'percussion': song_rythm_composed}
        
        return song

    def generation(self, pitch=4, mood='', scale='', seed=0):
        
        #///////////////////////////////////////////////////////////////////////////////////////////////////////
        #Getting seed
        if seed == 0:
            seed = random.randrange(int(sys.maxsize/8000))
            self.seed = seed
        else:
            self.seed = seed
            
        random.seed(self.seed)
        
        #Getting mood
        self.mood = mood

        #Getting pitch
        self.pitch = pitch

        #Getting scale and chords
        self.scale, self.scale_name, self.scale_chords = self.string_notes(pitch=pitch, sname=scale)



        #Getting chords progression
        self.progression = self.make_progression(self.scale_name)



        composed = self.Composer()


        #---------------------MUSIKONG-----------------------

        #"+str(mood)+"_"+str(seed)+"

        with open("songs/song_"+str(mood)+"_"+str(self.seed)+".json", "w") as write_file:
            json.dump(composed, write_file, indent=4)
        
        return [composed, self.seed]


