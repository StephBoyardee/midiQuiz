#import tkinter as tk
#from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
import random

import time
from time import sleep

import pickle

class myLabel(Frame):

    def nextChord(self):
        if self.App:
            self.App.nextChord()

    def onClick(self):
        if self.App:
            self.App.checkMidi()
        else:
            print("myLabelAppnotset")

    def __create_widgets(self):
        self.chordDescriptionTitle=StringVar()
        self.chordDescriptionTitle.set("TBD Chord")
        self.label = Label(self, text="Chord Description", anchor=CENTER, borderwidth=1, relief="solid")
        self.chordDescriptionLabel = Label(self, text=str(self.chordDescriptionTitle), textvariable=self.chordDescriptionTitle, font=('Samyak Devanagari', 32, "bold"), anchor=CENTER, borderwidth=1, relief="solid")
        self.label.grid(row=0, sticky=(S,W))
        self.chordDescriptionLabel.grid(row=1,sticky=(N,W))
        self.nextChordButton = Button(self, text="Next Chord", command=self.nextChord, borderwidth=1, relief="solid")
        self.nextChordButton.grid(row=2,sticky=(N,W))

        self.startTest = Button(self, text="Start Test", command=self.onClick, borderwidth=1, relief="solid")
        self.startTest.grid(row=3,sticky=(N,W))

    def __init__(self, _window, _chords):
        super().__init__(_window)
        self.chords=_chords
        self.__create_widgets();
        self.App=None

class mySearchableListbox(Frame):

    # Function for checking the 
    # key pressed and updating 
    # the listbox 
    def checkkey(self, event): 
           
        value = event.widget.get() 
        print(value)
          
        # get searchResultList from dataList
        if value == '': 
            self.searchResultList = self.dataList
        else: 
            self.searchResultList = [] 
            for item in self.dataList: 
                if value.lower() in item.lower(): 
                    self.searchResultList.append(item)                 
       
        # update searchResultList in listbox 
        self.updateSearchResultList()


       
       
    def updateSearchResultList(self): 
        # clear previous data 
        self.listbox.delete(0, 'end') 
       
        # put new data 
        for item in self.searchResultList: 
            self.listbox.insert('end', item) 

    def updateSelectedValuesText(self, event):
        self.curselectionValues=map(self.listbox.get, self.listbox.curselection())
        self.selectedValuesAsString.set(", ".join(self.curselectionValues))
        self.selectedValuesText.config(width=self.listbox.winfo_width()//self.monoCharPixelSize)

    def __create_widgets(self):
        self.label = Label(self, text=self.title)
        self.label.grid(column=0, columnspan=2, row=0, sticky=(N,S,E,W))

        self.selectedValuesText = Label(self, text=self.title, textvariable=self.selectedValuesAsString, font='TkFixedFont', height=4, width=20, anchor=NW, justify=LEFT)
        self.selectedValuesText.grid(column=0, columnspan=2, row=self.label.grid_info()['row']+1, sticky=(N,S,E,W))
        self.selectedValuesText.bind('<Configure>', lambda e: self.selectedValuesText.config(wraplength=self.winfo_width()))

        self.entry = Entry(self) 
        self.entry.grid(column=0, columnspan=2, row=self.selectedValuesText.grid_info()['row']+1, sticky=(N,S,E,W))
        self.entry.bind('<KeyRelease>', self.checkkey) 

        # Choosing selectmode as multiple  
        # for selecting multiple options 
        self.listbox = Listbox(self, selectmode = "multiple", exportselection=0)
        for each_item in range(len(self.dataList)): 
            self.listbox.insert(END, self.dataList[each_item])

        self.listbox.grid(column=0, row=self.entry.grid_info()['row']+1, sticky=(N,S,E,W))
        self.listbox.bind('<<ListboxSelect>>', self.updateSelectedValuesText)
        self.selectedValuesText.bind('<<ListboxSelect>>', lambda e: self.selectedValuesText.config(width=self.winfo_width()//self.monoCharPixelSize))

        # Creating a Scrollbar and  
        # attaching it to root window 
        self.scrollbar = Scrollbar(self) 
          
        # Adding Scrollbar to the right 
        # side of root window 
        self.scrollbar.grid(column=1, row=self.listbox.grid_info()['row'], columnspan=1, rowspan=1, sticky=(N,S,E,W), pady=5, padx=5)
        # Attaching Listbox to Scrollbar 
        # Since we need to have a vertical  
        # scroll we use yscrollcommand 
        self.listbox.config(yscrollcommand = self.scrollbar.set) 
          
        # setting scrollbar command parameter  
        # to listbox.yview method its yview because 
        # we need to have a vertical view 
        self.scrollbar.config(command = self.listbox.yview)

    def getSelectedValues(self):
        return list(self.curselectionValues)


    def __init__(self, _window, _title, _input_list):
        super().__init__(_window, width=100)
        self.searchResultList=[]
        self.selectedValuesAsString=StringVar()
        self.dataList=_input_list
        self.title=_title
        myFont = tkFont.Font(family='TkFixedFont')
        self.monoCharPixelSize = myFont.measure("X")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)

        self.__create_widgets()

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('MidiQuiz')
        self.geometry('800x800')
        #self.resizable(0, 0)
        self.resizable(1, 1)
        # windows only (remove the minimize/maximize button)
        self.attributes()

        fileName="midiQuizData.p"
        with open(fileName, 'rb') as dbfile: 
            payload = pickle.load(dbfile)
            (self.noteOn, self.noteOff, self.dOnOff, self.uniqueNotes, self.uniqueChordTypes, self.chordNumeralsRoman, self.dAnsiNotesWithOctave, self.dAnsiNotesWithoutOctave, self.dfChordsSimplified) = payload
        
        pg.init()
        md.init()
        self.selectedChordRoots=[]
        self.selectedChordTypes=[]

        #content = Frame(root, padding=(3,3,12,12))

        self.__create_widgets()


        # layout on the root window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)

    def __create_widgets(self):
        # create the input frame
        l2=["a","b","c","d","e","a","b","c","d","e","a","b","c","d","e","a","b","c","d","e","a","b","c","d","e","a","b","c","d","e"]  

        self.chordRootsListbox = mySearchableListbox(self, "Chords Roots", uniqueNotes)
        self.chordRootsListbox.grid(column=0, row=0, stick=(N, W))

        self.chordTypesListbox = mySearchableListbox(self, "Chord Types", uniqueChordTypes)
        self.chordTypesListbox.grid(column=2, row=0, stick=(N, E))

        self.sbox1 = mySearchableListbox(self, "Chords1", l2)
        self.sbox1.grid(column=2, row=2, stick=(S, E))

        self.sbox2 = mySearchableListbox(self, "Chords2", l2)
        self.sbox2.grid(column=0, row=2, stick=(S, W))

        self.chordPromptFrame = myLabel(self,l2)
        self.chordPromptFrame.grid(column=1, row=0, rowspan=3, stick=(N,W))
        self.chordPromptFrame.App=self

    def checkTestedChord(self, _notesOn):
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


    def generateRandomChordsList(self):
        dfw=self.dfChordsSimplified
        # selecting rows based on condition 
        selectedChords = dfw[dfw['CHORD_ROOT'].isin(self.selectedChordRoots) & 
                  dfw['CHORD_TYPE'].isin(selectedChordTypes)]
        self.randomizedSelectedChords=selectedChords.sample(n = selectedChords.shape[0], replace = False)

    def nextChord(self):
        if len(self.randomizedSelectedChords)>0:
            self.chordDescriptionTitle.set(self.randomizedSelectedChords.pop(0))
        else:
            self.generateRandomChordsList()
            self.chordDescriptionTitle.set(self.randomizedSelectedChords.pop(0))

    def checkMidi(self):
        self.selectedChordRoots = self.chordRootsListbox.getSelectedValues()
        self.selectedChordTypes = self.chordTypesListbox.getSelectedValues()
        delaySeconds = 10
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
            if self.checkTestedChord(notesOn):
                self.nextChord()
    
    continue


if __name__ == "__main__":
    app = App()
    app.mainloop()

    #Samyak Devanagari