from tkinter.messagebox import showinfo


from select_files import select_mp3_files
from edit_mp3_files import edit_metadata


def main():
    mp3_files = select_mp3_files()

    for path in mp3_files:
        edit_metadata(path)

    showinfo('Success', f'Metadata for {len(mp3_files)} files has been updated.')

if __name__ == '__main__':
    main()
