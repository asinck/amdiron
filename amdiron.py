#Adam Sinck
#This is a text editor I wrote for fun, and to see if I could

from Tkinter import *
import Tkinter as tk
import tkMessageBox

#global variables
currentTab = "Untitled 1" #this is the name of the initial tab
openDocuments = {}        #a hash table of documents
tabs = {}                 #a hash table of the tabs that will allow the
unnamedDocs = 1           #user to have multiple tabs open at once
#functions

#notDone will give a message saying that that feature is not complete
def notDone(var=None):
    tkMessageBox.showinfo("Not Ready", "This feature is not complete yet.")

#this will pop up a dialog box for user input
def popup(title, message, proceed, cancel, command, inputWidth=30):
    functionA = lambda: removePopup(userDialog, command, userInput.get())
    functionB = lambda(n): removePopup(userDialog, command, userInput.get())
    userDialog = tk.Toplevel()
    userDialog.title(title)
    label = Label(userDialog, text = message)
    userInput = Entry(userDialog, width = inputWidth)
    submit = Button(userDialog, text = proceed)
    submit.config(command=functionA)
    cancel = Button(userDialog, text=cancel, command = userDialog.destroy)
    label.pack()
    userInput.pack()
    submit.pack(side=RIGHT)
    cancel.pack(side=RIGHT)
    userInput.focus_set()
    userInput.bind("<Escape>", lambda(nothing): destroyThis(userDialog))
    userInput.bind("<Return>", functionB)

#this will kill the popup window and return the value it died with
def removePopup(window, command, value):
    window.destroy()
    command(value)

#this will remove any window given to it
def destroyThis(window):
    window.destroy()

#this will check to see if the current tab has been edited
def currentTabIsUnedited():
    return openDocuments[currentTab].get(1.0, END) == '\n'

#this is used for switching tabs
def edit(tabName, sameTab=False):
    global currentTab
    if not sameTab:
        tabs[currentTab].configure(bg = "#FFF")
    tabs[tabName].configure(bg = "#CCC")
    openDocuments[currentTab].pack_forget()
    openDocuments[tabName].pack()
    openDocuments[tabName].focus_set()
    currentTab = tabName

#make a new document
def openFile():
    popup("Open File", "What is the file name?", "Open", "Cancel", openAFile)

#this opens a file and allows the user to edit it
def openAFile(fileName):
    if fileName in tabs:
        tkMessageBox.showerror("Error", "This file is already open.")
        return
    try:
        text = open(fileName)
        s = ''
        for i in text:
            s += i
        text.close()
        if currentTabIsUnedited():
            #edit the current tab
            #change the display name of the current tab
            tabs[currentTab].configure(text = fileName)
            #make the command of the current tab be to edit the document with
            #the filename
            tabs[currentTab].configure(command = lambda: edit(fileName))
            #make a new entry in tabs, and make it point to the current tab
            #this makes it so that the key that points to the tab matches
            #the filename
            tabs[fileName] = tabs[currentTab]
            del tabs[currentTab]
            #put the file in the document area
            openDocuments[fileName] = Text(mainFrame, height=28, width=80)
            edit(fileName, True)
            openDocuments[fileName].insert(END, s)
            
        else:
            #make a new tab
            tabs[fileName] = (Button(tabsFrame, text = fileName))
            tabs[fileName].configure(command = lambda: edit(fileName))
            tabs[fileName].pack(side=LEFT)
            #put the file in the document area
            openDocuments[fileName] = Text(mainFrame, height=28, width=80)
            edit(fileName)
            openDocuments[fileName].insert(END, s)
        
    except:
        s = 'The file "' + fileName + '" cannot be opened.'
        tkMessageBox.showerror("Error", s)
    
#this saves the current tab's contents
def save(var=None):
    text = open(currentTab, 'w')
    contents = openDocuments[currentTab].get(1.0, END)
    text.write(contents)

#this pops up a window for saving a document with a different name
def saveAs(var=None):
    popup("Save As", "What is the new file name?", "Save", "Cancel", saveAsThis)

#this does the saving part of the save as
def saveAsThis(fileName):
    global currentTab, unnamedDocs
    #get the file name to save as; if it exists make sure that the user
    #meant to save the file with that name
    try:
        text = open(fileName, 'r')
        message = "This file already exists. Save anyway?"
        answer = tkMessageBox.askyesno("Error", message)
        if not answer:
            return
    except:
        pass
    if currentTab[0:8] == "Untitled":
        unnamedDocs -= 1
    
    #rename the current tab and make sure that it points at the right file
    tabs[fileName] = tabs[currentTab]
    del tabs[currentTab]
    tabs[fileName].configure(text = fileName)
    tabs[fileName].configure(command = lambda: edit(fileName))
    #rename the current document's key
    openDocuments[fileName] = openDocuments[currentTab]
    del openDocuments[currentTab]
    #update currentTab
    currentTab = fileName
    #write to file
    text = open(fileName, 'w+')
    contents = openDocuments[fileName].get(1.0, END)
    text.write(contents)

#this opens a new document
def newDoc(var=None):
    global currentTab, unnamedDocs
    unnamedDocs += 1
    s = "Untitled " + str(unnamedDocs)
    
    #make a tab
    tabs[s] = (Button(tabsFrame, text = s))
    tabs[s].configure(command = lambda: edit(s))
    tabs[s].pack(side=LEFT)
    
    #make the document
    openDocuments[s] = Text(mainFrame, height=28, width=80)
    edit(s)
    currentTab = s


#set up the gui

#top level stuff
root = Tk()
root.title("Text Editor")
try:
    icon = PhotoImage(file="te.png")
    root.tk.call('wm', 'iconphoto', root._w, icon)
except:
    print "Icon not found."
#menus
menubar = Frame(root, bg="#3C3B37")
menubar.pack(side=TOP, fill=BOTH)
fileMenu = Menubutton(menubar, text = 'File', underline = 0)
fileMenu.config(fg = "white", bg = "#3C3B37")
fileMenu.pack(side = LEFT)
menu = Menu(fileMenu)
menu.add_command(label = 'New document', command = newDoc, underline = 0)
menu.add_command(label = 'Open...', command = openFile, underline = 0)
menu.add_command(label = 'Save', command = save, underline = 0)
menu.add_command(label = 'Save As...', command =saveAs, underline = 5)
menu.add_command(label = 'Quit', command = quit, underline = 0)
fileMenu['menu'] = menu

#these are the tabs for multiple files
tabsFrame = Frame(root, bg = "#3C3B37")
tabsFrame.pack(side=TOP, fill=BOTH)

tabs["Untitled 1"] = (Button(tabsFrame, text = currentTab))
tabs["Untitled 1"].configure(command = lambda: edit("Untitled 1"))
tabs["Untitled 1"].configure(bg = "#CCC")
tabs["Untitled 1"].pack(side=LEFT)
mainFrame = Frame(root)
mainFrame.pack(side=TOP, fill=BOTH)

#initialize a document
openDocuments["Untitled 1"] = Text(mainFrame, height=28, width=80)
openDocuments["Untitled 1"].pack()
openDocuments["Untitled 1"].focus_set()
#setKeyBindings("Untitled 1")

root.mainloop()
