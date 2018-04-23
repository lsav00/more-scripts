#!/usr/bin/python3
import random

#this program plays the classic game of "War".
#It shuffles a deck of cards and converts the cards to numbers
#It constantly displays the cards for verification purposes

#the following contains the shuffling codes provided by the professor
cardfaces = ("A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2")
cardsuites = ("H", "S", "D", "C")

def init():
    thisdeck = []
    for suit in cardsuites:
        for face in cardfaces:
            thisdeck.append(face+suit)
    return thisdeck

def shuffle(mycards):
    unshuffled = mycards
    shuffled = []
    for count in range (0,len(unshuffled)):
        pick = ''
        while (pick == ''):
            pick = random.choice(unshuffled)
            shuffled.append(pick)
            unshuffled.remove(pick)	
    return shuffled

cards = init()                              #this creates the deck
cards = [card[:-1] for card in cards]       #this takes out the suites

#this converts the letter cards to numbers
cards = [card.replace("A", "14") for card in cards] 
cards = [card.replace("K", "13") for card in cards]
cards = [card.replace("Q", "12") for card in cards]
cards = [card.replace("J", "11") for card in cards]

#this converts all the string numbers into integers
cards = [int(card) for card in cards]

#this calls the shuffle method, provided by the professor
cards = shuffle(cards)

#the following divides the deck into equal piles for each player
computer = cards[0:26]
user = cards[26:53]

#this displays the initial hands of the players
print("Computer's hand is: ", computer)
print("User's hand is: ", user)

game_over = False   #initializes game_over variable to false
drawpile = []       #creates an empty drawpile list

while game_over == False:       #while loops until game_over is true
    draw = 0                #draw allows iteration thru hand indices during draws
    compdraw = computer[draw]   #this is computer's revealed card
    userdraw = user[draw]       #this is user's revealed card

    #these print statements give user a status of all cards for verification
    print()
    print()
    print("Computer's revealed card: ", compdraw)
    print("Your revealed card: ", userdraw)
    print("The drawpile has: ", drawpile)

    #tests and responds to computer wins & displays updated cards
    if compdraw > userdraw:         #if computer wins the draw...
        print("Computer wins")      #displays message that computer wins
        computer.append(compdraw)   #appends computer's card to comp's deck
        computer.append(userdraw)   #appends user's card to comp's deck
        computer.remove(compdraw)   #removes computer's card from comp's deck
        user.remove(userdraw)       #removes user's card from user's deck
        computer.extend(drawpile)   #adds drawpile cards to computer's deck
        drawpile = []               #empties drawpile deck
        print("Computer's new hand is: ", computer)
        print("User's new hand is: " , user)
        print("The drawpile has: ", drawpile)
        draw +=1
    #tests and responds to draws & displays updated cards
    elif compdraw == userdraw:      #if there's a draw...
        print("Draw")               #displays message of draw
        drawpile.append(compdraw)   #appends computer's card to drawpile
        drawpile.append(userdraw)   #appends user's card to drawpile
        computer.remove(compdraw)   #removes computer's card to comp's deck
        user.remove(userdraw)       #removes user's card from user's deck
        print("Computer's new hand is: ", computer)
        print("User's new hand is: " , user)
        print("The drawpile has: ", drawpile)
        draw += 1
    #tests and responds to user wins & displays updated cards
    else:                           #if user wins the draw...
        print("You win")            #displays message that user wins
        user.append(userdraw)       #appends user's card to user's deck
        user.append(compdraw)       #appends computer's card to user's deck
        user.remove(userdraw)       #removes user's card from user's deck
        computer.remove(compdraw)   #removes computer's card to comp's deck
        user.extend(drawpile)       #adds drawpile cards to user's deck
        drawpile = []               #empties drawpile deck
        print("Computer's new hand is: ", computer)
        print("User's new hand is: " , user)
        print("The drawpile has: ", drawpile)
        draw +=1
    #determines if game is over
    if len(computer) == 0:          #if computer's hand length is 0...
        print ("You won the game!") #displays message that user wins
        game_over = True            #and assigns game_over to True
    if len(user) == 0:              #if user's hand length is 0
        print("Sorry, you lost.")   #prints message that user loses
        game_over = True            #and assigns game_over to True


#REFERENCES:
#(1)Vig, C(2011, Sep. 10). StackOverflow. Convert all strings in a list to int
    #[duplicate]. Retrieved from: https://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int
#(2)Vazquez-Abrams (2010, Nov. 9). StackOverflow. Python count elements in list
    #[duplicate]. Retrieved from: https://stackoverflow.com/questions/4130027/python-count-elements-in-list
#(3)greggo(2015, Nov. 26). StackOverflow. How can I remove the last character of a
    #string in python? [duplicate]. Retrieved from: https://stackoverflow.com/questions/33940917/how-can-i-remove-the-last-character-of-a-string-in-python
#(4)sberry(2010, Jun. 28). StackOverflow. Find and replace string values in Python list
    #Retrieved from: https://stackoverflow.com/questions/3136689/find-and-replace-string-values-in-python-list