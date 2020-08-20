#!/usr/bin/env python
# coding: utf-8

# In[27]:


#importing necessary packages
import tkinter as tk
from PIL import Image,ImageDraw,ImageOps
import math
from numpy import random

#Read in from the high_scores.txt file tracking the high scores
#The format for the high scores is "{easy} {novice} {medium} {hard} {expert}"
#Reads into list as [easy,novice,medium,hard,expert]
try:
    file = open('high_scores.txt','r')
    high = file.read().split()
    high_score = [int(n) if n != 'None' else None for n in high]
    file.close()
#If the file doesn't exist, it'll set the high_score list to all None.
except FileNotFoundError:
    high_score = [None for n in range(5)]


#This creates a window with the label <instructions> and commands of yes and no functions
#All inputs are in string format
def yes_no_window(instructions, yes_func, no_func):
    global rootn
    rootn = tk.Tk()
    frame = tk.Frame(rootn)
    frame.pack()

    button = tk.Button(frame, 
                       text="Yes",
                       command=eval(yes_func))
    button.pack(side=tk.LEFT)

    button2 = tk.Button(frame, 
                       text="No",
                       command=eval(no_func))
    button2.pack(side=tk.LEFT)

    w2 = tk.Label(rootn, 
                  justify=tk.LEFT,
                  text=instructions).pack(side="left")

    rootn.mainloop()

#The game function with all windows  
def full_game():
    global root,wipe
    #The wipe function wipes the high_scores by setting list to all None
    def wipe():
        global rootn, sure_wipe
        rootn.destroy()
        #"Are you sure?" window
        def sure_wipe():
            global high_score
            high_score = [None for n in range(5)]
            rootn.destroy()
        instructions = 'Are you sure?'
        yes_no_window(instructions,'sure_wipe','rootn.destroy')
        
    instructions = "Wipe all high score data? This will remove all data of previous high scores done on this computer."
    
    yes_no_window(instructions,'wipe','rootn.destroy')
    
    #Directions to play
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    instructions = "Use S to move downwards and W to move upwards.    Don't get caught by Tom by moving through the gaps, and do not hit the walls."

    button = tk.Button(frame, 
                       text="Continue",
                       command=root.destroy)
    button.pack(side=tk.LEFT)

    w2 = tk.Label(root, 
                  justify=tk.CENTER,
                  text=instructions).pack(side="bottom")

    root.mainloop()


    #Player chooses difficulty
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    #difficulty assigns the input to the numb variable
    def difficulty(x):
        global numb
        numb = x
        root.destroy()

    prompt = "Difficulty?"

    #These inputs set the numb variable to some integer between 2 and 6
    #Numb represents the maximum columns of obstacles that can be fully on screen at once
    button0 = tk.Button(frame, 
                       text="Easy",
                       command=lambda: difficulty(2))
    button0.pack(side=tk.LEFT)

    button = tk.Button(frame, 
                       text="Novice",
                       command=lambda: difficulty(3))
    button.pack(side=tk.LEFT)

    button2 = tk.Button(frame, 
                       text="Medium",
                       command=lambda: difficulty(4))
    button2.pack(side=tk.LEFT)

    button3 = tk.Button(frame, 
                       text="Hard",
                       command=lambda: difficulty(5))
    button3.pack(side=tk.LEFT)

    button4 = tk.Button(frame, 
                       text="Expert",
                       command=lambda: difficulty(6))
    button4.pack(side=tk.LEFT)

    w2 = tk.Label(root, 
                  justify=tk.LEFT,
                  text=prompt).pack(side="top")

    root.mainloop()

    #Game function for the actual game and the after menus.
    def game():
        global counter, pos, playing, root2, numb, h, space
        #im is a blank black field
        im = Image.new("RGB", (1320, 660), 'black')
        #rand's length is equal to numb + 1. 
        #rand initializes with a random number for the last value and -1 everywhere else
        #rand is used to generate the gaps in the columns
        List = [n for n in range(10)]
        random.shuffle(List)
        rand = [-1 for n in range(numb)] + [List[0]]
        #counter is a base timer variable while pos is used to adjust obstacle positions
        #h is height of the player
        counter = -1
        pos = 11
        h = 295
        playing = True #whether the game is playing or not (becomes false when player "dies")
        #space is the distance between the left edges of adjacent obstacle columns
        space = int(1320/(len(rand) - 1))
        
        #Changes height of player if s or w is pressed
        def key(event):
            global h
            if event.char == 's':
                h += 20
            if event.char == 'w':
                h -= 20

        #The index of rand is needed to access the gaps
        #This increments the pos variable by space if pos gets to -88
        #It also shifts the values in the list the frame after, thus shifting the index needed
        def shift_list():
            global pos
            if pos == -88:
                pos += space
            if pos == space - 99:
                for x in range(len(rand) - 1):
                    rand[x] = rand[x + 1]
                while rand[-1] == rand[-2]:
                    random.shuffle(List)
                    rand[-1] = List[0]

        #This creates the image
        def create_image(pos):
            global space, h, place
            frame = im.copy()
            shift_list()
            #Pastes the Jerry image and saves the image before opening a tkinter PhotoImage
            frame.paste(Image.open("Icons\\Jerry.gif"),(100,h))
            #Generates the 11 slots for the Tom obstacles, leaving two open at random
            for x in range(len(rand)):
                if rand[x] != -1:
                    for n in range(9):
                        if n < rand[x]:
                            frame.paste(Image.open("Icons\\Tom.gif"),(space*x+pos,60*n))
                        else:
                            frame.paste(Image.open("Icons\\Tom.gif"),(space*x+pos,60*(n+2)))
            frame.save('field.gif')
            place = tk.PhotoImage(file = 'field.gif')

        #Function to start the counting and recursion
        def counter_label(label):
            counter = -1
            def count():
                global counter, pos, playing, root2, numb, ult_dest, restart
                #increments counter and pos. Timer is the current score.
                counter += 1
                timer = int(((counter-107) + abs(counter-107))/2)
                pos -= 11
                create_image(pos)
                #The below is essentially collision detection with the edges and obstacles
                #It sets playing to false which prevents recursion
                if h < 0 or h >= 620:
                    playing = False
                elif pos <= 140 and pos > 51 and rand[0] != -1:
                    if h < 60*rand[0] or (h + 40) >= 60*(rand[0] + 2):
                        playing = False
                #configures text and image labels
                label2.config(text=f'High Score: {high_score[numb-2]}      Score: {timer}')
                label.config(image=place)
                #recurs after 1ms if playing is true
                if playing:
                    label.after(1, count)
                #Otherwise it creates after-game windows
                else:
                    #sets the high score if needed
                    if high_score[numb-2] == None:
                        high_score[numb-2] = timer
                    elif timer > high_score[numb-2]:
                        high_score[numb-2] = timer
                    
                    #destroys all windows
                    def ult_dest():
                        global rootn
                        rootn.destroy()
                        root.destroy()

                    #destroys only the restart window and proceeds
                    def restart():
                        global rootn, change, scratch
                        rootn.destroy()
                        
                        #reruns the full game with pre-game windows
                        def change():
                            ult_dest()
                            full_game()
                            
                        #reruns from the game and onwards with unchanged settings
                        def scratch():
                            ult_dest()
                            game()

                        #Change or no change settings
                        instructions = "Change pre-game settings?"
                        yes_no_window(instructions,'change','scratch')
                        
                    #restart or no restart
                    instructions = "You failed. Restart?"
                    yes_no_window(instructions,'restart','ult_dest')

            #First iteration of the count function
            count()

        #Main game tkinter window configuration
        root = tk.Tk()
        root.title("Avoid the Obstacles")

        frame = tk.Frame(root)
        frame.pack()

        label = tk.Label(root)
        label.bind("<Key>",key)
        label.focus_set()
        label.pack()

        label2 = tk.Label(root)
        label2.pack()

        counter_label(label)

        button = tk.Button(frame,text="QUIT",command=root.destroy)
        button.pack()

        root.mainloop()
    
    #running the game after pre-game setup
    game()

#running the full game including setup
full_game()

#Writing the high_score list to the high_scores.txt file
file = open('high_scores.txt','w')
print_string = " ".join([str(score) for score in high_score])
file.write(print_string)
file.close()

