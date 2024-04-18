from django.shortcuts import render
import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO

def execute_python_code(request):
    root = tk.Tk()
    root.title("Hey Buddy ;)")
    root.overrideredirect(True)

    url = 'https://github.com/OrangesAreGreat10/Pi-server-file-share/blob/main/cup%20game%20web/cup.png?raw=true'
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    photo = ImageTk.PhotoImage(image)

    label = tk.Label(root, image=photo)
    label.pack()

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = 0
    y = 0
    root.geometry(f'+{x}+{y}')

    def on_closing():
        return None

    def close_program(event):
        if event.keycode == 49: #1
            print('press one to close')
            root.destroy()

    root.bind("<Key>", close_program) 

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    return render(request, 'templates/myapp/index.html')