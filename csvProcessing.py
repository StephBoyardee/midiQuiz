#pickle Data for game
import pickle
import pygame.midi as md

import pandas as pd
import numpy as np
from string import digits

dfChords=pd.read_csv("chord-new.csv", delimiter=",")
dfScales=pd.read_csv("music-scales-new.csv", delimiter=",", header=None)
dfChordsToMidiPitches=pd.read_csv("guitar-chords-midi-pitches-new.csv", delimiter=";")
dfChordProgressionsRoman=pd.read_csv("chord-porgressions-roman-numeral-new.csv", delimiter=";")

dfChordsSimplified=dfChords.copy()

uniqueNotes=list(dfChords.CHORD_ROOT.unique())
uniqueChordTypes=list(dfChords.CHORD_TYPE.unique())

#vii° assumes the leading tone is not raised. 
#Becomes VII° upon raising the first note of vii° a half step 
#vii° is in the minor key, but VII° is usually used and fits decently too
majorKeyChordProgressionMidiOffset = [ 0   ,  2     ,  4     ,  5    ,  7   ,  9    ,  13     ]
majorKeyChordProgression           = ['I'  , 'ii'   , 'iii'  , 'IV'  , 'V'  , 'vi'  , 'vii°'  ]
major7thKeyChordProgression        = ["I7" , "ii7"  , "iii7" , "IV7" , "V7" , "vi7" , "vii°7" ]
minorKeyChordProgressionMidiOffset = [ 0   ,  2     ,  3     ,  5    ,  7   ,  8    ,  9    ,  12    ,  13     ]
minorKeyChordProgression           = ['I'  , 'ii°'  , 'III'  , 'iv'  , 'V'  , 'v'   , 'VI'  , 'VII'  , 'vii°'  ]
minor7thKeyChordProgression        = ["i7" , "ii°7" , "III7" , "iv7" , "V7" , 'v7'  , "VI7" , "VII7" , "vii°7" ]

majorProgression = {"midiOffset": majorKeyChordProgressionMidiOffset,   \
                    "Maj":  majorKeyChordProgression,                   \
                    "Maj7": major7thKeyChordProgression                 }

minorProgression = {"midiOffset": minorKeyChordProgressionMidiOffset,   \
                    "m":  minorKeyChordProgression,                     \
                    "m7": minor7thKeyChordProgression                   }




noteOn=144
noteOff=128

dOnOff={}
dOnOff[noteOn]=1
dOnOff[noteOff]=0

remove_digits = str.maketrans('', '', digits)

midiToAnsiNoteOffset=21
dAnsiNotesWithOctave={}
dAnsiNotesWithoutOctave={}
ansiNotesWithoutOctaveList=[]
for i in range(21,109):
    dAnsiNotesWithOctave[i]=md.midi_to_ansi_note(i)
    dAnsiNotesWithoutOctave[i]=(md.midi_to_ansi_note(i).translate(remove_digits)) 
    ansiNotesWithoutOctaveList.append(md.midi_to_ansi_note(i).translate(remove_digits))

singleOctaveNotes=ansiNotesWithoutOctaveList[:12]
dfNotesUniqueDoubleSharpFlat=np.unique(dfChords.iloc[:, 3:9].to_numpy(str))
dictToNormalNotes={}
for i in dfNotesUniqueDoubleSharpFlat:
    if "##" in i:
        note=singleOctaveNotes.index(i[:-2])
        
        if note+2>11:
            note=note+2-12
        else:
            note=note+2
        normalNote=singleOctaveNotes[note]
        dictToNormalNotes[i]=normalNote
        
    elif "bb" in i:
        note=0
        if "b" in i[:-2]:
            note=singleOctaveNotes.index(i[:-3])-1
            
        else:
            note=singleOctaveNotes.index(i[:-2])
        if note-2<0:
            note=note-2+12
        else:
            note=note-2
        if "#" not in singleOctaveNotes[(note+1)%12]:
            normalNote=singleOctaveNotes[(note+1)%12]+"b"
        else:
            normalNote=singleOctaveNotes[(note+1)%12][:-1]
        print(i, normalNote)
        dictToNormalNotes[i]=normalNote

dfChordsSimplified=dfChords.replace({"Notes": dictToNormalNotes,"N/A": dictToNormalNotes,"N/A.1": dictToNormalNotes,"N/A.2": dictToNormalNotes,"N/A.3": dictToNormalNotes,"N/A.4": dictToNormalNotes,"N/A.5": dictToNormalNotes})


fileName="midiQuizData.p"
with open(fileName, 'wb') as dbfile: 
	payload=(noteOn, noteOff, dOnOff, uniqueNotes, uniqueChordTypes, majorKeyChordProgression, minorKeyChordProgression, dAnsiNotesWithOctave, dAnsiNotesWithoutOctave, dfChordsSimplified) 
	pickle.dump(payload, dbfile)

