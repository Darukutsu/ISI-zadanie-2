import time
import tkinter as tk
from tkinter import ttk
import random

medzera_medzi_krokmi = 0.4  # default rychlost.

## NOTE
# sachovnica je reprezentovana 1 rozmernym polom
# sachovnica[riadok] = stlpec --> na riadku N v stlpci M je kralovna
# ak sachovnica[riadok] = -1 tak pole je volne
#    0   1   2   3   4   5   6   7
#   ________________________________
# 0 |--||--||--||--||--||--||--||--|
# 1 |--||--||--||--||--||--||--||--|
# 2 |--||--||--||--||--||--||--||--|
# 3 |--||--||--||--||--||--||--||--|
# 4 |--||--||--||--||--||--||--||--|
# 5 |--||--||--||--||--||--||--||--|
# 6 |--||--||--||--||--||--||--||--|
# 7 |--||--||--||--||--||--||--||--|
#   ________________________________
sachovnica = []  # sachovnica a.k.a hlavne pole
velkost_sachovnice = 8  # default velkost
kroky = []  # Kroky vykonané algoritmom pre vizualizáciu
random_resety = 0  # counter random resetov pre Hill climbing


# Funkcia na overenie, či je umiestnenie kráľovnej na šachovnici validné
def valid(sachovnica, rows, col):
    for row in range(rows):
        # je na riadku alebo stlpci
        # NOTE:
        # dovolim si tvrdit ze je iba na rovnakom stlpci
        # nemusime checkovat riadky
        if sachovnica[row] == col:
            return False

        # je na diagonale
        # FIX:
        # a co ked sachovnica[row]=-1?
        if abs(sachovnica[row] - col) == abs(row - rows):
            return False

    # preslo
    return True


# DFS N-Queens
def dfs(sachovnica):
    global kroky
    kroky = []  # vynulovanie

    def solve(riadky=0):
        if riadky == velkost_sachovnice:  # vsetky kralovane su na sachovnici, solved...
            return True

        for stlpce in range(velkost_sachovnice):  # prejdi celu sachovnicu
            if valid(sachovnica, riadky, stlpce):  # isvalid ???
                sachovnica[riadky] = stlpce

                kroky.append(
                    list(sachovnica)
                )  # Ulož krok pre vizualizáciu neskor(originalne som mal len counter, ale GUI...)
                if solve(riadky + 1):  # Rekurzívne pokračuj na ďalší riadok
                    return True

                sachovnica[riadky] = -1  # Spätné vyhľadávanie (Backtracking) TU !!!!
                kroky.append(
                    list(sachovnica)
                )  # Ulož spätný krok pre vizualizáciu(znova len counter, neskor upravene na GUI)
        return False

    solve()


# prosim zabi ma, nenavidim toto
# dobra inspiracia
# https://www.youtube.com/watch?v=7fjmGWkv-sY&
# Problematika Hill climbing, optimum a random restard addition
# slight alternations, napriklad large steps, alebo max iterations niesu, bude bezat pokial sa nezrobi...
# https://en.wikipedia.org/wiki/Hill_climbing
# https://algorithmafternoon.com/stochastic/stochastic_hill_climbing_with_random_restarts/


def hill_climbing(sachovnica):
    global kroky, random_resety
    kroky = []  # vynulovanie krokov, znova najprv iba counter, upravene na trackovanie pre GUI
    random_resety = 0  # counter na pocitanie random_reset

    stav = []  # Inicializujeme prázdny zoznam pre stav šachovnice

    # Iteruj cez každý riadok šachovnice
    for nopodstatne in range(velkost_sachovnice):
        nahodny_stlpec = random.randint(
            0, velkost_sachovnice - 1
        )  # Generuj náhodný stĺpec pre daný riadok
        stav.append(nahodny_stlpec)  # radnom

    # Funkcia na spočítanie konfliktov na šachovnici
    def konflikt(stav):
        konflikty = 0  # Počiatočný počet konfliktov je 0

        # Prejdeme každú dvojicu kráľovien
        for i in range(len(stav)):
            for j in range(
                i + 1, len(stav)
            ):  # Porovnávame iba unikátne dvojice (bez opakovania)
                # Skontrolujeme, či sú kráľovné v tom istom stĺpci
                if stav[i] == stav[j]:
                    konflikty += 1

                # Skontrolujeme, či sú kráľovné na tej istej diagonále
                elif abs(stav[i] - stav[j]) == abs(i - j):
                    konflikty += 1

        return konflikty  # Vrátime celkový počet konfliktov

    # Nájde stav s minimálnym počtom konfliktov
    def najdi_minimalny_konflikt(stav):
        min_konflikt = konflikt(stav)
        najlepsi_stav = stav[:]

        for riadok in range(velkost_sachovnice):
            povodna_hodnota = stav[riadok]
            for novy_stlpec in range(velkost_sachovnice):
                if novy_stlpec == povodna_hodnota:  # Preskoč aktuálnu pozíciu
                    continue

                stav[riadok] = novy_stlpec
                novy_konflikt = konflikt(stav)

                if novy_konflikt < min_konflikt:  # akt. satv, menej konfliktov
                    min_konflikt = novy_konflikt
                    najlepsi_stav = stav[:]

            stav[riadok] = povodna_hodnota  # povodna hodnota
        return najlepsi_stav, min_konflikt

    while True:
        kroky.append(stav[:])  # Ulož aktuálny stav pre vizualizáciu
        stav, min_konflikt = najdi_minimalny_konflikt(stav)
        if min_konflikt == 0:  # konflik. 0, mame slovnute
            return stav
        if stav == kroky[-1]:  # lokalne optimum
            stav = []  # vynulovanie

            for zbytocne in range(velkost_sachovnice):  # iterate
                nahodny_stlpec = random.randint(
                    0, velkost_sachovnice - 1
                )  # Generujem náhodný stĺpec
                stav.append(nahodny_stlpec)  # add do zoznamu stavov

            random_resety += 1  # zvys pocet random state


# vykreslenie
def vykresli_sachovnicu(platno, kralovny):
    platno.delete("all")  # Vymaž
    velkost_policka = 600 // velkost_sachovnice  # zmenene kvoli N moze byt variabilne

    for i in range(velkost_sachovnice):  # Iterujeme cez všetky riadky šachovnice
        for j in range(velkost_sachovnice):  # Iterujeme cez všetky stĺpce šachovnice
            # farba bola, cez simple modulo
            if (i + j) % 2 == 0:
                farba = "white"
            else:
                farba = "black"

            # Vykreslenie jedného políčka pomocou metódy create_rectangle
            platno.create_rectangle(
                j * velkost_policka,  # X-súradnica lavy roh
                i * velkost_policka,  # Y-súradnica lavy roh
                (j + 1) * velkost_policka,  # X-súradnica pravy roh
                (i + 1) * velkost_policka,  # Y-súradnica pravy roh
                fill=farba,  # Farba políčka
            )

    for stlpce, riadky in enumerate(kralovny):
        if riadky != -1:
            y = riadky * velkost_policka + velkost_policka // 2
            x = stlpce * velkost_policka + velkost_policka // 2
            platno.create_oval(
                x - 0.5 * velkost_policka,
                y - 0.5 * velkost_policka,
                x + 0.5 * velkost_policka,
                y + 0.5 * velkost_policka,
                fill="red",
            )  # Nakreslí kráľovnú


# Zobrazenie krokov vizualizácie
def display_steps(platno, root):
    #  medzera_medzi_krokmi je teraz variabilna a moze byt zmenena uzivatelom
    global kroky, medzera_medzi_krokmi
    for krok in kroky:
        vykresli_sachovnicu(platno, krok)
        root.update()  # Aktualizuje GUI
        time.sleep(medzera_medzi_krokmi)  # Pauza medzi krokmi


# Zobrazenie štatistík algoritmov
def ukaz_staty(sachovnica, root):
    global kroky, random_resety

    # DFS štatistiky
    start_time_dfs = time.perf_counter()
    dfs(sachovnica)
    elapsed_time_dfs = time.perf_counter() - start_time_dfs
    steps_taken_dfs = len(kroky)

    # Hill-Climbing štatistiky
    random_resety = 0
    start_time_hc = time.perf_counter()
    hill_climbing(sachovnica)
    elapsed_time_hc = time.perf_counter() - start_time_hc
    steps_taken_hc = len(kroky)

    # Výpis štatistík
    stats_message = (
        f"Algorithm: DFS\n"
        f"Time Taken: {elapsed_time_dfs:.6f} seconds\n"
        f"Steps Taken: {steps_taken_dfs}\n\n"
        f"Algorithm: Hill-Climbing\n"
        f"Time Taken: {elapsed_time_hc:.6f} seconds\n"
        f"Steps Taken: {steps_taken_hc}\n"
        f"Random Resets: {random_resety}\n"
    )

    stats_window = tk.Toplevel(root)
    stats_window.title("Algorithm Statistics")
    tk.Label(stats_window, text=stats_message, justify="left", font=("Arial", 12)).pack(
        padx=10, pady=10
    )


# Výber algoritmu a vykonanie akcie
def executni_vyber(sachovnica, platno, root, typ_algoritmu, speed_var):
    global medzera_medzi_krokmi, velkost_sachovnice
    try:
        medzera_medzi_krokmi = float(speed_var.get())
    except ValueError:
        medzera_medzi_krokmi = 0.4  # Predvolená hodnota pri chybe
    sachovnica = [-1] * velkost_sachovnice  # Inicializácia šachovnice
    algoritmus = typ_algoritmu.get()
    if algoritmus == "DFS":
        dfs(sachovnica)
        display_steps(platno, root)
    elif algoritmus == "Hill-Climbing":
        hill_climbing(sachovnica)
        display_steps(platno, root)
    elif algoritmus == "Show Stats":
        ukaz_staty(sachovnica, root)
    elif algoritmus == "daj dole gate":
        print("Som spokojny s vladou slovenskej republiky, said no one, ever")
        # TODO
        # more gadzo petooo


# Vytvorenie GUI aplikácie
def gui():
    global sachovnica, velkost_sachovnice, medzera_medzi_krokmi

    def nastav_velkost():
        global velkost_sachovnice, sachovnica
        try:
            nova_velkost = int(size_entry.get())
            if nova_velkost < 4:
                raise ValueError
            velkost_sachovnice = nova_velkost
            sachovnica = [-1] * velkost_sachovnice
        except ValueError:
            tk.messagebox.showerror(
                "Invalid Input", "Please enter a valid size (4 or larger)."
            )

    root = tk.Tk()
    root.title("NQueens Solver")

    size_frame = tk.Frame(root)
    size_frame.pack()
    tk.Label(size_frame, text="Chessboard Size:").grid(row=0, column=0)
    size_entry = tk.Entry(size_frame)
    size_entry.grid(row=0, column=1)
    size_entry.insert(0, str(velkost_sachovnice))
    tk.Button(size_frame, text="Set Size", command=nastav_velkost).grid(row=0, column=2)

    platno = tk.Canvas(root, width=600, height=600, bg="white")
    platno.pack()

    control_panel = tk.Frame(root)
    control_panel.pack()

    tk.Label(control_panel, text="Algorithm:").grid(row=0, column=0)

    typ_algoritmu = tk.StringVar(value="DFS")
    algorithm_menu = ttk.Combobox(
        control_panel,
        textvariable=typ_algoritmu,
        values=["DFS", "Hill-Climbing", "Show Stats"],
    )
    algorithm_menu.grid(row=0, column=1)

    tk.Label(control_panel, text="Visualization Speed (sec):").grid(row=1, column=0)
    speed_var = tk.StringVar(value=str(medzera_medzi_krokmi))
    speed_entry = tk.Entry(control_panel, textvariable=speed_var)
    speed_entry.grid(row=1, column=1)

    tk.Button(
        control_panel,
        text="Execute",
        command=lambda: executni_vyber(
            sachovnica, platno, root, typ_algoritmu, speed_var
        ),
    ).grid(row=1, column=2)

    root.mainloop()


gui()
