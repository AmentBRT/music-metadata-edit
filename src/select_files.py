from tkinter.filedialog import askopenfilenames


def select_mp3_files():
    mp3_files = askopenfilenames(filetypes=[('MP3 Files', '*.mp3')])

    return mp3_files
