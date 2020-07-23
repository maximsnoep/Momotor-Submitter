#! python3
# graphics.py - graphical interface for the canvas submitter.

# imports
from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from submit import submit_to_canvas
import os


# tkinter graphical interface
def run():
    # initialize tkinter
    window = Tk()
    window.title("Canvas file submitter")

    # url input
    url_label = Label(window, text="Assignment URL", width=14, anchor="e")
    url_label.grid(column=0, row=0, padx=5, pady=10)
    url_entry = Entry(window, width=40)
    url_entry.grid(column=1, row=0, padx=5, pady=10)

    # username input
    user_label = Label(window, text="Username", width=14, anchor="e")
    user_label.grid(column=0, row=1, padx=5, pady=2)
    user_entry = Entry(window, width=40)
    user_entry.grid(column=1, row=1, padx=5, pady=2)

    # password input
    pass_label = Label(window, text="Password", width=14, anchor="e")
    pass_label.grid(column=0, row=2, padx=5, pady=2)
    pass_entry = Entry(window, show="*", width=40)
    pass_entry.grid(column=1, row=2, padx=5, pady=2)

    # file input
    input_files = ()

    def select_files(entry):
        nonlocal input_files
        input_files = (filedialog.askopenfilenames(parent=window, title='Choose files to submit'))
        entry.configure(state='normal')
        entry.delete('1.0', END)
        for i in range(len(input_files)):
            entry.insert('end', '[' + str(i) + '] ' + os.path.basename(input_files[i]) + "\n")
        entry.configure(state='disabled')

    file_label = Label(window, text="Files", width=14, anchor="e")
    file_label.grid(column=0, row=3, padx=5, pady=10)
    files_entry = ScrolledText(window, width=28, height=10, borderwidth=1)
    files_entry.grid(column=1, row=3, padx=5, pady=10)
    files_entry.insert('end', '[0] no files yet selected...\n')
    files_entry.configure(state='disabled')
    file_btn = Button(window, text="browse", width=10, command=lambda: select_files(files_entry))
    file_btn.grid(column=2, row=3, padx=5, pady=10)

    # submit button calls submit_to_canvas
    def submit(url, username, password, files):
        submit_to_canvas(url, username, password, files)

    submit_btn = Button(window, text="submit",
                        command=lambda: submit(url_entry.get(), user_entry.get(), pass_entry.get(), input_files))
    submit_btn.grid(column=1, row=99, padx=10, pady=20)

    total_width = 500
    total_height = 400
    window.geometry(str(total_width) + "x" + str(total_height))

    window.mainloop()
