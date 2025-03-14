from tkinter import *
from tkinter import filedialog
import os
import pygame

window = Tk()
window.title("Audio Visualizer")
window.geometry("1280x720")
window.resizable(False,False)
pygame.mixer.init()

frame = Frame(window)

c = Canvas(frame, bg="black", width=1280, height=635)
song_display = Listbox(frame, bg="black", fg="white", width=30, height=37)
song_display.grid(row=0,column=0, padx=5)

c.grid(row=0,column=1,padx=5)

frame.pack()

class MusicObj:
    songs = []
    curr_song = ""
    paused = False

music_obj = MusicObj

def load_music():
    window.directory = filedialog.askdirectory()
    for song in os.listdir(window.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3' or ext == '.wav' or ext == '.m4a' or ext == '.ogg' or ext == '.flac':
            music_obj.songs.append(song)

    for song in music_obj.songs:
        song_display.insert("end", song)

    song_display.selection_set(0)
    music_obj.curr_song = music_obj.songs[song_display.curselection()[0]]


toolbar = Menu(window)
window.config(menu=toolbar)
fileMenu = Menu(toolbar, tearoff=False)
fileMenu.add_command(label="Select", command=load_music)
toolbar.add_cascade(label="File",menu=fileMenu)

def play_music():

    if not music_obj.paused:
        pygame.mixer.music.load(os.path.join(window.directory, music_obj.curr_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        music_obj.paused = False

def pause_music():

    pygame.mixer.music.pause()
    music_obj.paused = True

def next_music():
    try:
        song_display.selection_clear(0,END)
        song_display.selection_set(music_obj.songs.index(music_obj.curr_song) + 1)
        music_obj.curr_song = music_obj.songs[song_display.curselection()[0]]
        play_music()
    except:
        pass

def prev_music():
    try:
        song_display.selection_clear(0,END)
        song_display.selection_set(music_obj.songs.index(music_obj.curr_song) - 1)
        music_obj.curr_song=music_obj.songs[song_display.curselection()[0]]
        play_music()
    except:
        pass


play_btn_img = PhotoImage(file='play-button.png')
pause_btn_img = PhotoImage(file='pause-button.png')
next_btn_img = PhotoImage(file='next-button.png')
prev_btn_img = PhotoImage(file='previous.png')

control_frame = Frame(window)
control_frame.pack()

play_btn = Button(master=control_frame, image=play_btn_img, borderwidth=0, command=play_music)
pause_btn = Button(master=control_frame, image=pause_btn_img, borderwidth=0, command=pause_music)
next_btn = Button(master=control_frame, image=next_btn_img, borderwidth=0, command=next_music)
prev_btn = Button(master=control_frame, image=prev_btn_img, borderwidth=0, command=prev_music)


play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

window.mainloop()
