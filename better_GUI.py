import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
# you just have to do this tkinter is rly fucked up
from wabballgorithm import matchmaker
import ast
global running_log
running_log = dict({'teams': {}, 'schedule': {}})
global oldlog
oldlog = False

def checkstarterlog(logold):
    log = ast.literal_eval(logold)
    if log == {} or log == None:
        return False
    elif isinstance(log, dict):
        if isinstance(log['teams'], dict) or isinstance(log['schedule'], dict):
            return True
    else:
        return False

# Function for opening the file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Text files", "*.txt*"), ("all files", "*.*"))
    )
    return filename
# reads utf8 encoded file
def read_utf8(file):
    with open(file , "r", encoding="utf-8") as f:
        return f.read()
# writes utf8 encoded file
def write_utf8(file , to_write):
    with open(file , "w", encoding="utf-8") as f:
        f.write(to_write)

def gui_one():
    root = tk.Tk()
    root.title("Wabber Matchmaker - Import previous matches")
    root.geometry("600x600")

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
                content = ast.literal_eval(read_utf8(filename))
                prev_data_entry.delete("1.0", tk.END)
                prev_data_entry.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file:\n{e}")

    tk.Button(root, text="Browse", command=load_file).pack(pady=10)

    def close_and_return():
        # get whatever text is in the box, store it, and close
        global running_log
        global oldlog
        print(f'balls + {running_log}')
        if checkstarterlog(prev_data_entry.get("1.0", tk.END)):
            running_log = ast.literal_eval(prev_data_entry.get("1.0", tk.END).strip())
            oldlog = True
        print(running_log) #\\\\\\\\
        root.destroy()

    tk.Button(root, text="Next", command=close_and_return).pack(pady=10)

    root.mainloop()

    gui_two(running_log)  # return after window closes

def gui_two(log):
    existing_struct = running_log["schedule"]

    root = tk.Tk()
    root.title("Wabber Matchmaker - Tournament setup")
    root.geometry("900x600")

    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    teams_frame = tk.Frame(root)
    teams_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(left_frame, text="Number of Tables:").pack()
    tables_entry = tk.Entry(left_frame)
    tables_entry.pack()
    tables_entry.insert(0, "4")

    tk.Label(left_frame, text="Number of Teams:").pack()
    teams_entry = tk.Entry(left_frame)
    teams_entry.pack()
    teams_entry.insert(0, '12')

    log_box = scrolledtext.ScrolledText(left_frame, width=55, height=20)
    log_box.pack(pady=10)

    # Keep references to the per-team Entry widgets
    team_entries = {}

    def update_team_entries(event=None):
        # create or remove entries to match the requested number
        try:
            n = int(teams_entry.get())
        except ValueError:
            return

        # remove extra widgets if n decreased
        existing = list(team_entries.keys())
        for idx in existing:
            if idx > n:
                widget = team_entries.pop(idx)
                widget['label'].destroy()
                widget['entry'].destroy()

        # add missing widgets if n increased
        for i in range(1, n + 1):
            if i not in team_entries:
                lbl = tk.Label(teams_frame, text=f"Team {i} name:")
                lbl.pack(anchor="w", padx=5, pady=2)
                ent = tk.Entry(teams_frame, width=30)
                ent.pack(padx=5, pady=(0,6))
                # prefill from running_log if present
                saved = running_log.get("teams", {}).get(i, ['', []])[0]
                if isinstance(saved, str) and saved:
                    ent.insert(0, saved)
                team_entries[i] = {'label': lbl, 'entry': ent}

    # update when the number-of-teams field changes or on focus-out
    teams_entry.bind("<KeyRelease>", update_team_entries)
    teams_entry.bind("<FocusOut>", update_team_entries)
    update_team_entries()

    def read_team_names_into_running_log():
        running_log.setdefault("teams", {})
        for i, widgets in team_entries.items():
            name = widgets['entry'].get().strip()
            # ensure the key exists
            if i not in running_log["teams"]:
                running_log["teams"][i] = ['', []]
            running_log["teams"][i][0] = name if name else f"Team {i}"

    def generate():
        # first persist team names typed so far
        read_team_names_into_running_log()

        try:
            n_tables = int(tables_entry.get())
            n_teams = int(teams_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Number of tables/teams must be integers.")
            return

        log_box.delete("1.0", tk.END)
        running_log["schedule"] = matchmaker(100, n_tables, n_teams, existing_struct)
        log_box.insert(tk.END, "Best Schedule:\n")
        for slot, matches in running_log["schedule"].items():
            log_box.insert(tk.END, f"Slot {slot}: {matches}\n")

    tk.Button(left_frame, text="Generate Schedule", command=generate).pack(pady=10)

    def close_and_return():
        # persist names before closing
        read_team_names_into_running_log()
        print("final running_log:", running_log)
        root.destroy()

    tk.Button(left_frame, text="Next (wahoo)", command=close_and_return).pack(pady=10)

    root.mainloop()

    gui_three(running_log.get("schedule"))


def gui_three(schedule):
    if running_log["schedule"] == None:
        raise ValueError('No schedule provided')
    
    root = tk.Tk()
    root.title("Wabber Matchmaker - Score tournament")
    root.geometry("600x600")
    
    # I still need to adapt the scoring thing to this, it's going to be crazy. 
    # Also still needs to keep saving the log to a file in case of some dumbass closing the window.
    # But then maybe it will work!! And you can score it!! and have it be constantly updating a log file!!
    # and oh the scoring screen needs a button thet can based on the log file open gui 2 again and set more matches up
    # But then it might finally work!!!!!!!!!!!!!!!!  


gui_one()










