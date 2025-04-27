#import tkinter
from tkinter import *
from tkinter import filedialog
import os
import pygame
import ollama
import requests
import base64
#import time

#Setup
url = 'http://127.0.0.1:7860/sdapi/v1/txt2img' #local url of stable diffusion webui
client = ollama.Client()
model = "gemma3:4b" #change name if using different model
window = Tk()
window.title("Audio Visualizer")
window.geometry("1280x720")
window.resizable(False,False)
pygame.mixer.init()

frame = Frame(window)

c = Canvas(frame, bg="black", width=960, height=635)

song_display = Listbox(frame, bg="black", fg="white", width=30, height=37)
song_display.grid(row=0,column=0, padx=5)
c.grid(row=0,column=1,padx=5)

frame.pack()


#Music object class containing list of songs loaded, the current song, and whether music is paused
class MusicObj:
    songs = []
    curr_song = ""
    paused = False

music_obj = MusicObj

#Allow user to choose a playlist/folder of music to load into program
def load_music():
    c.delete("all")
    window.directory = filedialog.askdirectory()
    for song in os.listdir(window.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3' or ext == '.wav' or ext == '.m4a' or ext == '.ogg' or ext == '.flac':
            music_obj.songs.append(song)

    for song in music_obj.songs:
        song_display.insert("end", song)

    song_display.selection_set(0)
    music_obj.curr_song = music_obj.songs[song_display.curselection()[0]]

#Allow user to select audio files in program toolbar
toolbar = Menu(window)
window.config(menu=toolbar)
fileMenu = Menu(toolbar, tearoff=False)
fileMenu.add_command(label="Select", command=load_music)
toolbar.add_cascade(label="File",menu=fileMenu)
c.create_text(960/2, 635/2, text="Select song folder using 'File' menu", fill="white", anchor="center")

#Image class containing image file information,list of created images, and creation of image in tkinter canvas
class Image:
    def __init__(self,x,y,img,anc):
        self.img_file = PhotoImage(file=img)
        self.images = list()
        self.image = c.create_image(x,y,image=self.img_file,anchor=anc)

#Create image object
c.ai_img = ai_img = Image(c.winfo_width()/2,c.winfo_height()/2,"","center")

#Prompt gemma3 and stable diffusion, then display image on canvas
def display_img():
    c.delete("all")
    prompt_ai()
    ai_img = Image(c.winfo_width()/2,c.winfo_height()/2,"img_outputs/output.png",'center')
    ai_img.images.append(ai_img)
    print(ai_img.images)

#Checking for the event the current song ends
pygame.init()
SONG_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(SONG_END)

def check_end():
    for event in pygame.event.get():
        if event.type == SONG_END:
            return True
    return False

#Play the music and display generated images on screen
def play_music():
    if not music_obj.paused:
        pygame.mixer.music.load(os.path.join(window.directory, music_obj.curr_song))
        c.create_text(c.winfo_width()/2,c.winfo_height()/2,text="generating...", fill = "white", anchor="center")
        c.update()
        pygame.mixer.music.play()
        while not check_end() and not music_obj.paused:
            display_img()
            c.update()
        else:
            ai_img.images.clear()
            if check_end():
                next_music()
    else:
        pygame.mixer.music.unpause()
        music_obj.paused = False
        while not check_end() and not music_obj.paused:
            display_img()
            c.update()
        else:
            ai_img.images.clear()
            if check_end():
                next_music()

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

#Create control buttons
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

#Prompting LLM and feeding the response to Stable Diffusion for image generation, saving the output
def prompt_ai():
    prompt = "Tell me a detailed stable diffusion image prompt that captures the emotions and vibe you can analyze in this song:" + os.path.join(window.directory, music_obj.curr_song) + "without any comments or explanations. Give me only the prompt."
    response = client.generate(model=model, prompt=prompt)
    print(response.response)

    #Create stable diffusion payload to send to api, then receive response and extract image file
    payload = {
        "prompt": response.response,
        "steps": 20,
    }
    api_response = requests.post(url=url, json=payload)
    r = api_response.json()

    save_path = os.path.join(os.getcwd()+'/img_outputs', "output.png")
    with open(save_path, 'wb') as f:
        f.write(base64.b64decode(r['images'][0]))


window.mainloop()
