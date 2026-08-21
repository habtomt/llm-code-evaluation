import pyttsx3
import os

def narrate (text ):
    engine =pyttsx3 .init ()
    engine .say (text )
    engine .runAndWait ()

def clear_screen ():
    os .system ('cls'if os .name =='nt'else 'clear')

def handle_invalid_input (prompt ):
    while True :
        user_input =input (prompt ).strip ().lower ()
        if user_input in ['left','right','explore','stay','enter','back']:
            return user_input
        else :
            print ("Invalid choice. Please try again.")

def interactive_story ():

    clear_screen ()
    narrate ("Welcome to our interactive storytelling experience. Your journey will depend on the choices you make.")

    clear_screen ()
    narrate ("You find yourself in a dark forest. Would you like to go left towards the faint light or right towards the darker path?")
    choice1 =handle_invalid_input ("Enter 'left' or 'right': ")

    if choice1 =="left":

        clear_screen ()
        narrate ("You head towards the faint light and discover an enchanted village. The villagers greet you warmly.")
        narrate ("You have a feast with them. Would you like to explore more or stay the night?")
        choice2 =handle_invalid_input ("Enter 'explore' or 'stay': ")

        if choice2 =="explore":

            clear_screen ()
            narrate ("You explore the village and find a wise old wizard who shares with you the secrets of the forest.")
            narrate ("You leave the village with newfound knowledge.")
        elif choice2 =="stay":

            clear_screen ()
            narrate ("You decide to stay the night. In the morning, you wake up to the sounds of birds and the warm sun on your face.")
        else :

            clear_screen ()
            narrate ("Not a valid choice, the villagers look puzzled and send you back home.")

    elif choice1 =="right":

        clear_screen ()
        narrate ("You follow the darker path and encounter a mysterious cave.")
        narrate ("Would you like to enter the cave or turn back?")
        choice2 =handle_invalid_input ("Enter 'enter' or 'back': ")

        if choice2 =="enter":

            clear_screen ()
            narrate ("You enter the cave and discover hidden treasures guarded by a friendly dragon.")
            narrate ("The dragon shares its knowledge and treasures with you as a friend.")
        elif choice2 =="back":

            clear_screen ()
            narrate ("You decide the cave is too risky and head back to the forest entrance.")
        else :

            clear_screen ()
            narrate ("Not a valid choice, you find yourself lost.")

    else :

        clear_screen ()
        narrate ("Not a valid choice. Please start the story again to continue.")

if __name__ =="__main__":
    try :
        interactive_story ()
    except Exception as e :
        print ("An error occurred: ",str (e ))