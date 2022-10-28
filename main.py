from msilib.schema import ComboBox
from tkinter import *
from tkinter import ttk
from turtle import bgcolor, width
from PIL import Image, ImageTk
from random import seed
from scamp import *
from algoritmo import *
from music_player import *
import multiprocessing as mp

procedural = Algorithm()

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def set_tempo():
    pass

def pick_mood(e):
    if mood.get() == 'aggressive' or mood.get() == 'melancholic':
        scale.config(values=list(procedural.scales['minor scales'].keys()))
        scale.current(0)
    if mood.get() == 'epic':
        scale.config(values=list(procedural.scales['major scales'].keys()))
        scale.current(0)

def gen():
    pnote = notes.index(pitch.get())
    pseed = seed.get()
    try:
        pseed = int(pseed)
    except:
        pseed = 0

    generated, gseed = procedural.generation(mood=mood.get(), pitch=pnote, scale=scale.get(), seed=pseed)

    seedLabel.config(text='Seed was: ' + str(gseed))

    ptempo = tempo.get()
    try:
        ptempo = int(ptempo)
    except:
        ptempo = 0

    
    active = mp.active_children()

    if active:
        for child in active:
            child.kill()
        
    p1 = mp.Process(target=play_song, args=(ptempo, mood.get(), gseed, partValue.get(),))
    p1.start()

root = Tk()
canvas = Canvas(root, width=800, height=600, bg='gray')
canvas.grid(columnspan=5, rowspan=5)

myLabel = Label(root, text='Music Djentnerator!', bg='gray')
myLabel.grid(column=2, row=0)

#Imagen extraida de: 
# https://www.facebook.com/Random-Music-Generator-215557581866270/photos/221141614641200
image = Image.open('./images/image.jpg')
image = image.resize((200,200))
image = ImageTk.PhotoImage(image)
image_label = Label(image=image)
image_label.image = image
image_label.grid(column=0, row=0)


#Tempo
tempoLabel = Label(root, text='Tempo', bg='gray')
tempoLabel.grid(column=0, row=1)
tempo = Entry(root, width=5)
tempo.grid(column=0, row=2)

#Pitch
pitchLabel = Label(root, text='Set a key note', bg='gray')
pitchLabel.grid(column=0, row=3)
pitch = ttk.Combobox(root, state='readonly', values=notes)
pitch.grid(column=0, row=4)
pitch.current(4)

#Mood
moodLabel = Label(root, text='Select a mood', bg='gray')
moodLabel.grid(column=3, row=0)
mood = ttk.Combobox(root, state='readonly', values=procedural.moods)
mood.current(0)
mood.grid(column=3, row=1)
mood.bind("<<ComboboxSelected>>", pick_mood)

#Scale
scaleLabel = Label(root, text='Select a scale', bg='gray')
scaleLabel.grid(column=3, row=2)
scale = ttk.Combobox(root, state='readonly', values=[" "])
scale.current(0)
scale.grid(column=3, row=3)

#Seed:
seedLabel = Label(root, text='Seed was: ', bg='gray')
seedLabel.grid(column=2, row=1)
seed = Entry(root, width=7)
seed.grid(column=2, row=2)

#Partitura
partValue = BooleanVar()
partitura = ttk.Checkbutton(root, text='Generate music sheet', variable=partValue)
partitura.grid(column=3, row=4)



generate = Button(root, command=lambda: gen(), text='Generate')
generate.grid(column=2, row=4)

if __name__ == '__main__':
    root.mainloop()