import time
import tkinter as tk
from tkinter import ttk

medzera_medzi_krokmi = 0.4

# Global variables
sachovnica = [-1,-1,-1,-1,-1,-1,-1,-1]
# sachovnica[4] = 7 - Riadok 4, kralovna na pozicii 7
# sachovnica[2] = -1 - Riadok 2, kralovna sa nenachadza

kroky = []
# Kroky pre vizualizaciu

# zisti ci je validne
def valid(sachovnica, riadky, stlpce):
    # Stlpce && Riadky
    for i in range(riadky):
        if sachovnica[i] == stlpce:
            return False

    # Diagonaly
    for i in range(riadky):
        if abs(sachovnica[i] - stlpce) == abs(i - riadky):
            return False

    # ak prejde, je valid(safe :D)
    return True

def dfs(sachovnica):
    global kroky
    kroky = []  # vynuluj

    # Rrekurzivne riesenie ako je dane v DFS
    def solve(riadky=0):
        if riadky == 8:  # Vsetky riadky presli
            return True

        for stlpce in range(8):  # prejdi vsetky a uloz kralovne
            # Prva iteracia je vzdy valid
            if valid(sachovnica, riadky, stlpce):  # Je pozicia valid ?
                sachovnica[riadky] = stlpce
                kroky.append(list(sachovnica))  # zaznamenaj krok
                if solve(riadky + 1):
                    return True
                sachovnica[riadky] = -1  # Backtrack
                kroky.append(list(sachovnica))  # zaznamenaj krok
        return False

    solve()

# vizualizacia
def vykresli_sachovnicu(platno, kralovny):
    platno.delete("all")
    
    velkost_policka = 600 // 8

    # vykresli policka
    for i in range(8):
        for j in range(8):

            # modulo, black 'n white
            if (i + j) % 2 == 0:
                farba = "white"
            else:
                farba = "black"

            platno.create_rectangle(j * velkost_policka, i * velkost_policka,(j + 1) * velkost_policka, (i + 1) * velkost_policka, fill=farba)

    for stlpce, riadky in enumerate(kralovny):
        if riadky != -1:
            y = riadky * velkost_policka + velkost_policka // 2
            x = stlpce * velkost_policka + velkost_policka // 2

            platno.create_oval(x - 20, y - 20, x + 20, y + 20, fill="red")

# Display the solution krok-by-krok
def display_steps(platno, root):
    global kroky
    for krok in kroky:
        vykresli_sachovnicu(platno, krok)
        root.update()
        time.sleep(medzera_medzi_krokmi)

# Show the statistics of the DFS algorithm
def ukaz_staty(sachovnica, root):
    global kroky
    start_time = time.perf_counter()
    dfs(sachovnica)
    elapsed_time = time.perf_counter() - start_time
    steps_taken = len(kroky)

    # Display the stats in a popup window
    stats_window = tk.Toplevel(root)
    stats_window.title("Algorithm Statistics")
    stats_message = (f"Algorithm: DFS\n"
                     f"Time Taken: {elapsed_time:.6f} seconds\n"
                     f"kroky Taken: {steps_taken}")
    tk.Label(stats_window, text=stats_message, justify="left", font=("Arial", 12)).pack(padx=10, pady=10)

# Act ak vyber
def executni_vyber(sachovnica, platno, root, typ_algoritmu):
    algoritmus = typ_algoritmu.get()
    if algoritmus == "DFS":
        dfs(sachovnica)
        display_steps(platno, root)

    elif algoritmus == "dalsi_algoritmus":
        print("todo Peto more gadzo Volosin Nigga Sosak ")

    elif algoritmus == "Show Stats":
        ukaz_staty(sachovnica, root)

# Create the GUI
def gui():
    global sachovnica
    root = tk.Tk()
    root.title("NQueens Solver - Inteligentne Systemy - Peter Matkulcik & Daniel Rusnak")

    platno = tk.Canvas(root, width=600, height=600, bg="white")
    platno.pack()

    control_panel = tk.Frame(root)
    control_panel.pack()

    tk.Label(control_panel, text="Algorithm:").grid(row=0, column=0)

    typ_algoritmu = tk.StringVar(value="DFS")

    algorithm_menu = ttk.Combobox(control_panel, textvariable=typ_algoritmu, values=["DFS", "Show Stats"])

    algorithm_menu.grid(row=0, column=1)

    tk.Button(control_panel, text="executni_vyber", command=lambda: executni_vyber(sachovnica, platno, root, typ_algoritmu)).grid(row=0, column=2)

    root.mainloop()

# displajni GUI, defakto znamena, ze uzivalte moze zacat
gui()
