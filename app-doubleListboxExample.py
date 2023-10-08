#import tkinter as tk
#from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont

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
        curselectionValues=map(self.listbox.get, self.listbox.curselection())
        self.selectedValuesAsString.set(", ".join(curselectionValues))
        print("x: ", self.grid_bbox(column=0, row=4),self.grid_bbox(column=0, col2=1, row=4))
        self.selectedValuesText.config(width=self.listbox.winfo_reqwidth()//self.monoCharPixelSize)


    def __create_widgets(self):
        self.label = Label(self, text=self.title)
        self.label.grid(column=0, columnspan=2, row=0, sticky=(N,S,E,W))

        self.selectedValuesText = Label(self, text=self.title, textvariable=self.selectedValuesAsString, font='TkFixedFont', height=4, width=20, anchor=NW, justify=LEFT)
        self.selectedValuesText.grid(column=0, columnspan=2, row=self.label.grid_info()['row']+1, sticky=(N,S,E,W))
        self.selectedValuesText.bind('<Configure>', lambda e: self.selectedValuesText.config(wraplength=self.winfo_reqwidth()))

        self.entry = Entry(self) 
        self.entry.grid(column=0, columnspan=2, row=self.selectedValuesText.grid_info()['row']+1, sticky=(N,S,E,W))
        self.entry.bind('<KeyRelease>', self.checkkey) 

        # Choosing selectmode as multiple  
        # for selecting multiple options 
        self.listbox = Listbox(self, selectmode = "multiple", exportselection=0)
        for each_item in range(len(self.dataList)): 
            self.listbox.insert(END, self.dataList[each_item]) 
          
            # coloring alternative lines of listbox 
            #self.listbox.itemconfig(each_item, bg = "white")

        self.listbox.grid(column=0, row=self.entry.grid_info()['row']+1, sticky=(N,S,E,W))
        self.listbox.bind('<<ListboxSelect>>', self.updateSelectedValuesText)
        self.selectedValuesText.bind('<<ListboxSelect>>', lambda e: self.selectedValuesText.config(width=self.winfo_reqwidth()//self.monoCharPixelSize))

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

        self.update_idletasks()
        print(self.winfo_reqwidth(),self.monoCharPixelSize)

        self.selectedValuesText.config(width=self.winfo_reqwidth()//self.monoCharPixelSize)
        print("x: ", self.grid_bbox(column=0, row=4),self.grid_bbox(column=0, col2=1, row=4))


    def __init__(self, _window, _title, _input_list):
        super().__init__(_window, width=100)
        print("!!width: ", self.winfo_reqwidth())
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

        #content = Frame(root, padding=(3,3,12,12))

        self.__create_widgets()

        # layout on the root window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def __create_widgets(self):
        # create the input frame
        l2=["a","b","c","d","e","a","b","c","d","e","a","b","c","d","e","a","b","c","d","e","a","b","c","d","e","a","b","c","d","e"]  

        sbox1 = mySearchableListbox(self, "Chords", l2)
        sbox1.grid(column=0, row=0, stick=(N, W))

        sbox1 = mySearchableListbox(self, "Chords", l2)
        sbox1.grid(column=1, row=0, stick=(N, E))

        sbox1 = mySearchableListbox(self, "Chords", l2)
        sbox1.grid(column=1, row=1, stick=(S, E))

        sbox1 = mySearchableListbox(self, "Chords", l2)
        sbox1.grid(column=0, row=1, stick=(S, W))


        # create the button frame
        #sbox2 = mySearchableListbox(self)
        #sbox2.grid(column=1, row=0)


if __name__ == "__main__":
    app = App()
    app.mainloop()