import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
# you just have to do this tkinter is rly fucked up
from wabballgorithm import matchmaker
import ast

# Function for opening the file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Text files", "*.txt*"), ("all files", "*.*"))
    )
    return filename

def read_utf8(file):
    with open(file , "r", encoding="utf-8") as f:
        return f.read()

def write_utf8(file , to_write):
    with open(file , "w", encoding="utf-8") as f:
        f.write(to_write)

def gui_one():
    root = tk.Tk()
    root.title("Wabber Matchmaker - Import previous matches")
    root.geometry("600x600")

    loaded_content = tk.StringVar()  # store file content here

    # --- File Content Display ---
    tk.Label(root, text="File Contents:").pack(pady=(10, 0))
    prev_data_entry = tk.Text(root, width=70, height=20)
    prev_data_entry.pack(padx=10, pady=5)
    prev_data_entry.insert(tk.END, '{}')

# --- Browse Button ---
    def load_file():
        filename = browseFiles()
        if filename:
            try:
                content = read_utf8(filename)
                loaded_content.set(content)  # save it to variable
                prev_data_entry.delete("1.0", tk.END)
                prev_data_entry.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file:\n{e}")

    tk.Button(root, text="Browse", command=load_file).pack(pady=10)

    def close_and_return():
        # get whatever text is in the box, store it, and close
        loaded_content.set(prev_data_entry.get("1.0", tk.END).strip())
        root.destroy()

    tk.Button(root, text="Next", command=close_and_return).pack(pady=10)

    root.mainloop()

    gui_two(loaded_content.get())  # return after window closes

def gui_two(previous):
    root = tk.Tk()
    root.title("Wabber Matchmaker - Tournament setup")
    root.geometry("600x600")

    tk.Label(root, text="Number of Tables:").pack()
    tables_entry = tk.Entry(root)
    tables_entry.pack()
    tables_entry.insert(0, "4")

    tk.Label(root, text="Number of Teams:").pack()
    teams_entry = tk.Entry(root)
    teams_entry.pack()
    teams_entry.insert(0, "12")

    log_box = tk.scrolledtext.ScrolledText(root, width=55, height=20)
    log_box.pack(pady=10)

    best = None

    def generate():
    
        n_tables = int(tables_entry.get())
        n_teams = int(teams_entry.get())
        existing_struct = ast.literal_eval(previous)
        log_box.delete("1.0", tk.END)

        best = matchmaker(100, n_tables, n_teams, existing_struct)
        log_box.insert(tk.END, "Best Schedule:\n")
        for slot, matches in best.items():
            log_box.insert(tk.END, f"Slot {slot}: {matches}\n")

    tk.Button(root, text="Generate Schedule", command=generate).pack(pady=10)

    def close_and_return():
        # get whatever text is in the box, store it, and close
        root.destroy()

    tk.Button(root, text="Next (wahoo)", command=close_and_return).pack(pady=10)

    root.mainloop()

    gui_three(best)

def gui_three(schedule):
    if schedule == None:
        raise ValueError('No schedule provided')
    
    root = tk.Tk()
    root.title("Wabber Matchmaker - Score tournament")
    root.geometry("600x600")
    
    # I still need to adapt the scoring thing to this, it's going to be crazy.
    # And then i will have to change the data structure of the initial import and everything and that's going to be swell
    # But then maybe it will work!! And you can score it!! and have it be constantly updating a log file!!
    # and oh the scoring screen needs a button thet can based on the log file open gui 2 again and set more matches up
    # But then it might finally work!!!!!!!!!!!!!!!!  

gui_one()










