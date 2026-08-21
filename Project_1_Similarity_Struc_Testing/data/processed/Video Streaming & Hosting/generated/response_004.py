import tkinter as tk
from tkinter import messagebox

root =tk .Tk ()
root .title ("Interactive Video")

video_label =tk .Label (root ,text ="Video Player")
video_label .pack ()

def show_quiz ():

    quiz_label .pack ()

    annotations_label .pack_forget ()

def check_answer (answer ):
    if answer =='Paris':
        messagebox .showinfo ("Result","Correct!")
    else :
        messagebox .showinfo ("Result","Try again.")

quiz_label =tk .Label (root ,text ="Quiz Time!",font =("Arial",24 ))
quiz_label .pack_forget ()
quiz_question_label =tk .Label (root ,text ="What is the capital of France?")
quiz_question_label .pack_forget ()
button1 =tk .Button (root ,text ="Paris",command =lambda :check_answer ('Paris'))
button1 .pack_forget ()
button2 =tk .Button (root ,text ="London",command =lambda :check_answer ('London'))
button2 .pack_forget ()
button3 =tk .Button (root ,text ="Berlin",command =lambda :check_answer ('Berlin'))
button3 .pack_forget ()

annotations_label =tk .Label (root ,text ="Annotations")
annotations_label .pack_forget ()

start_button =tk .Button (root ,text ="Start Video",command =show_quiz )
start_button .pack ()

root .mainloop ()