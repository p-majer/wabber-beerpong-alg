import tkinter as tk
from wabballgorithm import matchmaker
import ast

# Function for opening the 
# file explorer window
def browseFiles():
    filename = tk.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))

def run_gui():
    root = tk.Tk()
    root.title("Beerpong Matchmaker")
    root.geometry("900x600")

    # --- Layout Frames ---
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- Left Frame ---
    tk.Label(left_frame, text="Previous matches (as dict):").pack()
    prev_entry = tk.Entry(left_frame, width=50)
    prev_entry.pack()
    prev_entry.insert(0, "{}")

    tk.Label(left_frame, text="Number of Tables:").pack()
    tables_entry = tk.Entry(left_frame)
    tables_entry.pack()
    tables_entry.insert(0, "4")

    tk.Label(left_frame, text="Number of Teams:").pack()
    teams_entry = tk.Entry(left_frame)
    teams_entry.pack()
    teams_entry.insert(0, "12")

    log_box = tk.scrolledtext.ScrolledText(left_frame, width=50, height=20)
    log_box.pack(pady=10)

    # --- Right Frame for Results Input (Scrollable) ---
    results_label = tk.Label(right_frame, text="Enter Match Results:")
    results_label.pack()

    canvas = tk.Canvas(right_frame)
    scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Optional: Enable mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    scores = {}  # {(team1, team2): {'winner': x, 'loser': y}}

    def save_results():
        try:
            for match, fields in scores.items():
                winner = fields["winner_entry"].get()
                loser = fields["loser_entry"].get()
                if not winner or not loser:
                    continue  # skip empty
                scores[match]["winner"] = int(winner)
                scores[match]["loser"] = int(loser)
            tk.messagebox.showinfo("Saved", "All match results saved successfully!")
            print("Saved Scores:", {k: {"winner": v["winner"], "loser": v["loser"]} for k, v in scores.items()})
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save results:\n{e}")

    def generate():
        # Clear previous fields
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        try:
            n_tables = int(tables_entry.get())
            n_teams = int(teams_entry.get())
            existing_struct = ast.literal_eval(prev_entry.get())

            best = matchmaker(100, n_tables, n_teams, existing_struct)
            log_box.insert(tk.END, "Best Schedule:\n")

            row = 0
            for slot, matches in best.items():
                log_box.insert(tk.END, f"Slot {slot}: {matches}\n")

                tk.Label(scrollable_frame, text=f"Slot {slot}", font=("Arial", 10, "bold")).grid(row=row, column=0, pady=5)
                row += 1

                for match in matches:
                    tk.Label(scrollable_frame, text=f"Match {match}").grid(row=row, column=0, sticky="w", padx=5)

                    winner_entry = tk.Entry(scrollable_frame, width=5)
                    winner_entry.grid(row=row, column=1, padx=5)
                    tk.Label(scrollable_frame, text="Winner").grid(row=row, column=2)

                    loser_entry = tk.Entry(scrollable_frame, width=5)
                    loser_entry.grid(row=row, column=3, padx=5)
                    tk.Label(scrollable_frame, text="Loser").grid(row=row, column=4)

                    scores[tuple(match)] = {
                        "winner_entry": winner_entry,
                        "loser_entry": loser_entry,
                        "winner": None,
                        "loser": None
                    }
                    row += 1

            log_box.insert(tk.END, "\n---\n")
            # tk.messagebox.showinfo("Done", "Schedules generated and input fields created!")
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    tk.Button(left_frame, text="Generate Schedule", command=generate).pack(pady=10)
    tk.Button(right_frame, text="Save Results", command=save_results).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
