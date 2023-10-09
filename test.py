import pygame as pg
import pygame.event as ev
import pygame.midi as md

import pandas as pd
import numpy as np
from string import digits

import pickle

fileName="midiQuizData.p"
with open(fileName, 'rb') as dbfile: 
    (noteOn, noteOff, dOnOff, uniqueNotes, uniqueChordTypes, chordNumeralsRoman, dAnsiNotesWithOctave, dAnsiNotesWithoutOctave, dfChordsSimplified) = pickle.load(dbfile)

print("xxxxxx",noteOn)

#print(d)


def generateRandomChordsList():
    dfw=dfChordsSimplified
    # selecting rows based on condition 
    selectedChords = dfw[dfw['CHORD_ROOT'].isin(selectedChordRoots) & 
              dfw['CHORD_TYPE'].isin(selectedChordTypes)]
    randomizedSelectedChords=selectedChords.sample(n = selectedChords.shape[0], replace = False)

def checkTestedChord(_notesOn):
    testedChord = dfw[(dfw['CHORD_ROOT']==testedChordRoot) & 
              (dfw['CHORD_TYPE']==testedChordType)]
    testedChordNotes=testedChord.iloc[:, 3:10]
    numCorrectNotes=0
    for i in _notesOn:
        #False if any note is not in the chord
        if (testedChordNotes!=i).any().any():
            return False
        #False if chord is missing
        if (testedChordNotes==i).any().any():
            numCorrectNotes+=1
    nan_count = testedChordNotes.isna().sum().sum()
    if numCorrectNotes+nan_count==7:
        return True
    return False


pg.init()
md.init()

#print(md.get_count())
#print(md.get_default_input_id())

#i = 0
#info_list = []
#while md.get_device_info(i) is not None:
#    current_info = md.get_device_info(i)
#    info_list.append(current_info)
#    i += 1

#pg.display.set_mode((1, 1))


import time
from time import sleep
delaySeconds = 1000
close_time = time.time()+delaySeconds
midi_in=md.Input(3)

notesOn = []
while close_time>time.time():
    
    sleep(.1)
    midi_data=md.Input.read(midi_in, 100)

    for i in range(len(midi_data)):
        midi_note, timestamp = midi_data[i]
        print(timestamp, midi_note[0], midi_note[1], midi_note[2])

        if midi_note[0]==noteOn:
            notesOn.append(d[midi_note[1]])

        elif midi_note[0]==noteOff:
            notesOn.remove(d[midi_note[1]])

        print(notesOn)
    
    continue
md.quit()

