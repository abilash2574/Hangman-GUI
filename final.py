"""
    A hangman Game
    This class contains all the GUI elements
"""


#------------Importing Files needed for this class------------------------------

from tkinter import *
from tkinter import messagebox
import turtle
import random
#------------------Creating the main files for GUI------------------------------
# R2 - The `global` statement doesn't expose variables to other scopes like this
global word_list, chance, tested_letters, limit

word_list = [
    "funny",
    "overjoy",
    "joke",
]

chance = 0

tested_letters = []

limit = len(word_list)-1
# R2 - There isn't a selected_word as a global variable anywhere
global selected_word

def restart():      # We can recall this function to restart the game
        selected_word = list(word_list[random.randint(0,limit)])
        global chance
        chance = 0
        for child in start.result_frame.winfo_children():
            child.destroy()
        for child in start.test_frame.winfo_children():
            child.destroy()
        start.fragments(selected_word)
        start.basic()


def check(selected_word):
    # R2 Disable button to prevent spamming - mainly due to animation
    start.check_button.config(state=DISABLED)
    enter_value = start.query_entry.get()
    start.query_entry.delete(0, END)
    if enter_value in selected_word:    # This part display when we correctly guess a letter
        get_index = selected_word.index(enter_value)
        start.display_ans(enter_value, get_index)
        selected_word[get_index] = None
        if len(set(selected_word)) == 1:
            start.won()
    else:   # This part draws the hangman when we guess a wrong letter
        global chance, tested_letters
        tested_letters.append(enter_value)
        start.display_test(tested_letters)
        chance +=1
        if chance == 1: start.chance_1()
        if chance == 2: start.chance_2()
        if chance == 3: start.chance_3()
        if chance == 4: start.chance_4()
        if chance == 5: start.chance_5()
        # if chance !=5 : chance += 1
        if chance == 6:
            start.chance_6()
            tested_letters=[]
            chance=0
            start.lost()

    # R2 Re-enable button
    start.check_button.config(state=NORMAL)


main = Tk()
main.title("Hangman Game")
main.geometry('750x485')

#--------------------Creating the class for design------------------------------

class design:
    def __init__(self):
        #-----------------Main-frames-------------------------------------------
        self.main_frame = LabelFrame(main, height=100, width=100)
        self.main_frame.grid(row=0, column=0, sticky=N)
        # R2 - Unnecessary assignment to `self` as it's used nowhere else
        self.draw_frame = LabelFrame(main, bd=2, height=400, width=600)
        self.draw_frame.grid(row=0, column=1)
        self.canva = Canvas(master = self.draw_frame, height=473, width=400)
        self.canva.grid(row = 0, column = 1)
        #-------------This frame holds the widget for asking query--------------
        self.query_frame = LabelFrame(self.main_frame, height = 250, width = 150, bd=2)
        self.query_frame.grid(row=0,column=0)
        #----------------This frame is for the Button---------------------------
        # self.check_button = Button(self.main_frame, text="Check the letter", command=lambda: check(selected_word))
        # self.check_button.grid(row=1,column=0)
        #------------------This frame is for displaying the wrong guesses-------
        self.test_frame = LabelFrame(self.main_frame, text="Tested Characters", height=40, width=150, bd=2)
        self.test_frame.grid(row=2, column=0)
        #------------------This frame is to show the correct guessed letters----
        self.result_frame = LabelFrame(self.main_frame, height=100, width=500, bd=2)
        self.result_frame.grid(row=3, column=0)
        #----------------Turtle Starting code-----------------------------------
        self.hang = turtle.RawTurtle(self.canva)
        #-----------------------------------------------------------------------
        self.query = Label(self.query_frame, text="Enter the word you expect")
        self.query.grid(row=1, column=0,pady=5)
        self.query_entry = Entry(self.query_frame, width=10)
        self.query_entry.grid(row=1, column=1, padx=5)
                # R2 - Disable the button to prevent running both animations at the same time
        self.close_buttton = Button(self.main_frame, text="Exit", state=DISABLED, command=lambda: self.close())
        self.close_buttton.grid(row=4, column=0)

        self.result_label = Label(self.result_frame, text="The Word Order")
        self.result_label.grid(row=0, column=0)
        self.query_entry = Entry(self.query_frame, width=10)
        self.query_entry.grid(row=1, column=1, padx=5)
        #-----------------------------------------------------------------------

    # This function has all the widgets that are placed in the different frames
    def fragments(self, selected_word):
        # R2 - These next seven lines are duplicated

        # R2 - Duplicate of the following 6 lines
        self.tested_letters=[]
        self.test_label = Label(self.test_frame, text=self.tested_letters)
        self.test_label.grid(row=0, column=0)
        # R2 - Disable the button to prevent running both animations at the same time
        self.check_button = Button(self.main_frame, text="Check the letter", state=DISABLED, command=lambda: check(selected_word))
        self.check_button.grid(row=1,column=0)

        # R2 - As the children of test_frame are never cleared, there are both the words and blanks from
        # before, so you need to destroy them. As you're not keeping track of them anywhere, you'll
        # have to iterate through the children of test_frame manually. Since we know it's all the
        # children after the second label, you can do that like so:
        # for child in self.test_frame.winfo_children()[:2]:
        #     child.destroy()

        #--------------------------------------------------------------------------------
        # This will display empty dashes giving a clue about the total letters in the word
        for i in range(len(selected_word)):
            # R2 - Unnecessary assignment to `self` as it's used nowhere else
            self.output_label = Label(self.result_frame, text="_ ")
            self.output_label.grid(row=1, column=i, sticky=E)

    # This function is to show the correctly guessed letters
    def display_ans(self, enter_value, get_index):
        # R2 - Unnecessary assignment to `self` as it's used nowhere else
        self.output_label = Label(self.result_frame, text=enter_value+" ")       # We display the Entered value into the GUI for reference
        self.output_label.grid(row=1, column=get_index, sticky=E)

    # This function is to display the wrong guessed letters
    def display_test(self, tested_letters):
        # R2 - Unnecessary assignment to `self` as it's used nowhere else
        self.tested_label = Label(self.test_frame, text=''.join(tested_letters))  # To display it in the GUI
        self.tested_label.grid(row=0, column=0)

    # This function is used to create the stage of the hangman in the canvas
    def basic(self):
        # This is for making the stage
        # R2 - Turtle is based on vectors, so you need to
        # manually reset the position and direction like so
        self.hang.setposition(0.0, 0.0)
        self.hang.setheading(0.0)

        # R2 - The screen can be cleared with the clear() method
        self.hang.clear()

        self.hang.penup()
        self.hang.right(90)
        self.hang.forward(200)
        self.hang.left(90)
        self.hang.pendown()
        self.hang.begin_fill()
        for i in range(2):
            self.hang.forward(100)
            self.hang.right(90)
            self.hang.forward(30)
            self.hang.right(90)
        self.hang.end_fill()
        self.hang.forward(50)
        self.hang.left(90)
        self.hang.forward(300)
        self.hang.left(90)
        self.hang.forward(80)
        self.hang.left(90)
        self.hang.forward(50)

        # R2 - Re-enable button
        self.check_button.config(state=NORMAL)
        self.close_buttton.config(state=NORMAL)
    def chance_1(self):
        # Head starts
        self.hang.penup()
        self.hang.right(90)
        self.hang.forward(29)
        self.hang.left(90)
        self.hang.forward(28)
        self.hang.pendown()
        self.hang.circle(30)


    def chance_2(self):
        # Body
        self.hang.penup()
        self.hang.forward(31)
        self.hang.left(90)
        self.hang.forward(30)
        self.hang.right(90)
        self.hang.pendown()
        self.hang.forward(120)

    def chance_3(self):
        # First legs
        self.hang.left(40)
        self.hang.forward(60)
        self.hang.penup()
        self.hang.backward(60)
        self.hang.pendown()

    def chance_4(self):
        # Second legs
        self.hang.right(80)
        self.hang.forward(60)
        self.hang.penup()
        self.hang.backward(60)
        self.hang.left(40)
        self.hang.pendown()

    def chance_5(self):
        # First hand
        self.hang.penup()
        self.hang.backward(70)
        self.hang.pendown()
        self.hang.left(45)
        self.hang.forward(60)

    def chance_6(self):
        # Last hand
        self.hang.penup()
        self.hang.backward(60)
        self.hang.right(90)
        self.hang.pendown()
        self.hang.forward(60)
        #--------------------------------------------------------------------------------

    # This function is used to close the game with an message
    def close(self):
        messagebox.showinfo("GoodBye!", "Thanks For Playing")
        main.destroy()


    # This function is to quit or restart the game if we are lost
    def lost(self):
        # R2 - Unnecessary assignment to `self` as it's used nowhere else
        self.temp = messagebox.askokcancel("Game Over!","You lost and hanged \nPress 'Ok' to Retry and 'Cancel' to Quit")
        # for child in self.result_frame.winfo_children()[:2]:
        #     child.destroy()
        global chance, tested_letters
        tested_letters = []
        if self.temp:

            restart()
            # canvas.delete(self.canvas)
            # starting(chance, word_list)
        else:
            self.close()
    # This function is used when we win the game to either restart or to quit
    def won(self):
        # R2 - Unnecessary assignment to `self` as it's used nowhere else
        self.temp = messagebox.askokcancel("You Won!", "You won the Game \nPress 'Ok' to Play again and 'Cancel' to Quit")
        # for child in self.result_frame.winfo_children()[:2]:
        #     child.destroy()
        global chance, tested_letters
        tested_letters=[]
        if self.temp:
            restart()
            # starting(chance, word_list)
        else:
            self.close()
    # This function just greets the user
    def greeting(self):
        # R2 - Unnecessary assignment to `self` as it's used nowhere else
        self.welcome = messagebox.askyesno("Welcome", "Press 'Yes' to play")
        return self.welcome

# The GUI starts from calling the design class from here

start = design()

#This is for making a welcome popup and also to quit

if start.greeting():
    restart()          # This function can be used to keep on calling the whole program and also to change the word to guess
else:
    start.close()

main.mainloop()
