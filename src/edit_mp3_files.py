from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.id3 import TIT2, TPE1, TALB, TCON, COMM, TDRC, PCNT, TPE1, TPE2, TRCK

from tkinter import Tk, Label, Entry, Button, StringVar, Toplevel
from tkinter.messagebox import showinfo

from os.path import basename


root = Tk()
root.withdraw()


def edit_metadata(file_path, **kwargs):
    try:
        audio = ID3(file_path)
    except ID3NoHeaderError:
        showinfo('Error', f'No ID3 header found in {file_path}. Cannot edit.')
        return

    tags = {}

    for tag in ('Title', 'Artist', 'Album', 'Genre', 'Comment', 'Year', 'Play_Counter', 'Album_Artist', 'Track_Number'):
        if tag in kwargs:
            tags[tag] = kwargs[tag]

    if len(tags) == 0:
        tags.update(show_form(audio))

    save_changes(audio, tags)


def show_form(audio):
    top = Toplevel(root)

    filename = basename(audio.filename)
    top.title(f'Edit Metadata of "{filename}"')

    current_tags = get_tags(audio)

    entries = {}
    for i, (tag_name, value) in enumerate(current_tags.items()):
        Label(top, text=tag_name + ':').grid(row=i, column=0, sticky='e')

        var = StringVar(value=value)
        entry = Entry(top, textvariable=var)
        entry.grid(row=i, column=1, sticky='ew')

        entries[tag_name] = entry


    def add_changes():
        for tag_name, entry in entries.items():
            current_tags[tag_name] = entry.get()

        showinfo('Success', f'Metadata for {audio.filename} has been updated.')


    Button(top, text='Save Changes', command=add_changes).grid(row=len(current_tags)+1, column=0, columnspan=2, pady=20)

    top.wait_window()

    return current_tags


def get_tags(audio):
    return {
        'Title': audio.getall('TIT2')[0][0] if len(audio.getall('TIT2')) > 0 else '',
        'Artist': audio.getall('TPE1')[0][0] if len(audio.getall('TPE1')) > 0 else '',
        'Album': audio.getall('TALB')[0][0] if len(audio.getall('TALB')) > 0 else '',
        'Genre': audio.getall('TCON')[0][0] if len(audio.getall('TCON')) > 0 else '',
        'Comment': audio.getall('COMM::eng')[0][0] if len(audio.getall('COMM::eng')) > 0 else '',
        'Year': str(audio.getall('TDRC')[0][0]) if len(audio.getall('TDRC')) > 0 else '',
        'Play_Counter': str(audio.getall('PCNT')[0].count) if len(audio.getall('PCNT')) > 0 else '',
        'Album_Artist': str(audio.getall('TPE2')[0][0]) if len(audio.getall('TPE2')) > 0 else '',
        'Track_Number': str(audio.getall('TRCK')[0][0]) if len(audio.getall('TRCK')) > 0 else '',
    }


def save_changes(audio, tags):
    for tag_name, var in tags.items():
        match tag_name:
            case 'Title':
                frame = TIT2(encoding=3, text=var)
            case 'Artist':
                frame = TPE1(encoding=3, text=var)
            case 'Album':
                frame = TALB(encoding=3, text=var)
            case 'Genre':
                frame = TCON(encoding=3, text=var)
            case 'Comment':
                frame = COMM(encoding=3, text=var)
            case 'Year':
                frame = TDRC(encoding=3, text=var)
            case 'Play_Counter':
                frame = PCNT(encoding=3, text=var)
            case 'Album_Artist':
                frame = TPE2(encoding=3, text=var)
            case 'Track_Number':
                frame = TRCK(encoding=3, text=var)

        audio.add(frame)

    audio.save()
