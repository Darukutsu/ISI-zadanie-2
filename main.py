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

# MINMAX
# ALG
# minmax je 2player algoritmus pri ktorom si urcime hlbku do akej budeme
# chciet evaluevovat hodnoty binarneho stromu. Hrac1 preferuje hodnoty vyssie a Hrac2 nizsie.
# Kazdy node na rovnakej urovni ma rovnakeho vlastnika. Vlastnici sa striedaju medzi urovnami
#               1
#           2       2
#          1 1     1 1      <-- posledna uroven ma iba hodnoty z ktory sa vybera do vyssej
#              ...          <-- viac urovni
# hraci si vyberaju podla svojho nastavenia hodnoty z nodu
# e.g. ak hrac 1 ma na vyber medzi 4 a 7 vyberie si 7 pretoze je vyssia a on preferuje vyssie
#
# IMPLEMENTACIA
# kedze nasa hra nie je pre 2 hracov rozhodol som sa upravit tuto implementaciu.
# kazdy node ma ako hodnotu pocet queens v danych validnych tahoch.
# depth = pocet validnych tahov
# depth=depth+1 lebo posledna uroven su iba hodnoty
# tahy su random, ak sa pri overovani sachovnice zisti ze nejaky tah je neplatny recalculujeme
# neplatne tahy? || alebo vsetko pre dany node UVIDIM
# potom na zaklade urovne(lvl) sa rozhodne ktore node uprednostnime a napisemeho do nodu
#              MAX
#         MIN       MIN
#       MIX MAX   MIX MAX
#              ...          <-- viac urovni
# probably stupid idea skip this
#
# def minmax(sachovnica, depth, ismore):


# Inspiration https://www.youtube.com/watch?v=X6m0DXt95bs
# Forward checking MRV, LCV
# Forward checking - eliminates boxes which our queen can move
# MRV - picks up column with lowest possible choices, executes LCV if at more than 1 col empty
#       otherwise put queen into col if only 1 choice
# LCV - choose box which takes out least possible boxes


def FML(chessboard, board_size):
    global kroky
    kroky = []  # vynulovanie
    # puts first queen in random place
    # row = random.randrange(board_size)
    # col = random.randrange(board_size)
    prev_moves = []
    valid_stack = []

    # start in top left corner
    for row in range(board_size):
        for col in range(board_size):
            valid_stack = forward_checking(board_size, (row, col))
            prev_moves[0] = (row, col)
            chessboard[row] = col
            kroky.append(list(chessboard))
            queens = 1

            while queens < board_size:
                if not prev_moves:
                    break
                if queens == board_size:
                    # congrat you found solution, do something and continue
                    #    return chessboard
                    return
                if queens + valid_stack.size() < board_size:
                    # clears whole stack
                    # for i in len(prev_moves):
                    #    chessboard[prev_moves[i][0]]=-1
                    # backtrack
                    # break
                    chessboard[prev_moves.pop()[0]] = -1
                    kroky.append(list(chessboard))
                    queens -= 1
                    # this is almost unneccessary but I don't know how to optimize
                    valid_stack = forward_checking(
                        board_size, prev_moves[len(prev_moves) - 1]
                    )
                    continue

                optimal_row = MRV(valid_stack)
                # only 1 option left, set board to abs value
                if optimal_row < 0:
                    chessboard[abs(optimal_row)] = valid_stack[abs(optimal_row)]
                    prev_moves.append((abs(optimal_row), valid_stack[abs(optimal_row)]))
                # multiple options on optimal_row perform lcv
                else:
                    lcv = LCV(board_size, optimal_row, valid_stack, prev_moves)
                    valid_stack = lcv[1]
                    chessboard[optimal_row] = lcv[2]

                kroky.append(list(chessboard))
                queens += 1

        # clear
        chessboard[row] = -1
        kroky.append(list(chessboard))

    # return


def forward_checking(board_size, wherequeenplaced: (int, int)):
    valid_stack = []
    for row in range(board_size):
        if row + 1 == wherequeenplaced[0] or row - 1 == wherequeenplaced[0]:
            # . . . X X X . .
            # . . . . 4 . . .
            # . . . X X X . .
            # . . . . . . . .
            # . . . . . . . .
            # . . . . . . . .
            # . . . . . . . .
            # . . . . . . . .
            valid_stack[row] = [
                *range(wherequeenplaced[1] - 1),
                *range(wherequeenplaced[1] + 2, board_size),
            ]
            # elif row = wherequeenplaced[0]
            # we don't need this
            # . . . . . . . .
            # X X X X 4 X X X
            # . . . . . . . .
            # . . . . . . . .
            # . . . . . . . .
            # . . . . . . . .
            # . . . . . . . .
            # . . . . . . . .
        elif row != wherequeenplaced[0]:
            # . . . . . . . .
            # . . . . 4 . . .
            # . . . . . . . .
            # . . X . X . X .
            # . X . . X . . X
            # X . . . X . . .
            # . . . . X . . .
            # . . . . X . . .
            valid_stack[row] = [
                # left diagonal
                *range(wherequeenplaced[1] - abs(row - wherequeenplaced[0])),
                # mid col diagonal
                *range(
                    wherequeenplaced[1] - abs(row - wherequeenplaced[0]) + 1,
                    wherequeenplaced[1],
                ),
                *range(
                    wherequeenplaced[1] + 1,
                    wherequeenplaced[1] + abs(row - wherequeenplaced[0]),
                ),
                # right diagonal
                *range(
                    wherequeenplaced[1] + abs(row - wherequeenplaced[0]), board_size
                ),
            ]

    return valid_stack


# we do row based approach
# each row consists of valid value, row with least amount of valid values is picked
def MRV(board_size, valid_stack):
    min = board_size
    for row in range(board_size):
        row_len = len(valid_stack[row])
        if row_len == 1:
            return -row
        elif row_len < min and row_len != 0:
            min = row

    return min


def LCV(board_size, row, valid_stack, backtracking_stack):
    least_constaint_stack = []
    _backtracking_stack = []

    # for i, col in enumerate(valid_stack[row], start=0):
    for col in valid_stack[row]:
        new_valid_stack = forward_checking(board_size, (row, col))
        duplicates = len(set(new_valid_stack) - set(valid_stack))

        # intentional jumping
        # least_constaint_stack[col] = (duplicates, new_valid_stack)
        (duplicates, new_valid_stack, col)
        # least_constaint_stack.append(duplicates)
        # least_constaint_stack.append(forward_checking(board_size, (row, col)).size())
        # least_constaint_stack[i] = forward_checking(board_size, (row, col)).size()
        _backtracking_stack.append((row, col))

    smallest = min(least_constaint_stack, key=lambda x: x[0])

    # we do it this way to move smallest item first in fifo
    for item in _backtracking_stack:
        if item != smallest:
            backtracking_stack.append(item)
    backtracking_stack.append(smallest)

    return smallest
    # return col since we know row
    # return least_constaint_stack.index(min(least_constaint_stack))


# NOTE:
# Maybe move this inside DFS
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


# This is my try on implementing hillclimb
# later I discover coleague already implemented it, leave this as comment
# Hillclimbing
# randomize state, put on each row queen
# check for conflicts, store checkboards with conflicts in stack
# choose checkboard with lowest possible conflicts, and repeat
# Inspiration
# https://www.youtube.com/watch?v=7fjmGWkv-sY&
#
# if stack_size 0 stack is set to 10 but imediatelly when board with less conflicts appear
# it is chosen and stack is discarted
# def hillclimb(velkost_sachovnice):
#    stack = []
#    stack_size=(velkost_sachovnice-1)*velkost_sachovnice
#
#    def generate_board():
#        checkboard = []
#        for row in range(velkost_sachovnice):
#            checkboard[row] = random.randrange(velkost_sachovnice)
#        return checkboard
#
#    for i in range(stack_size):
#        stack[i] = generate_board()
#
#    def return_conflicts(checkboard, velkost_sachovnice):
#        conflicts=0
#
#        # each queen generates same conflicts so at the end divide by 2
#        # optimization could be check only downward
#        for row in range(velkost_sachovnice):
#            if checkboard[row] == col
#                conflicts+=1
#
#            if abs(sachovnica[row] - col) == abs(row - rows):
#                conflicts+=1
#        return conflicts/2
#
#    def least_conflicts(stack):
#        conflicts=


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

    # Forwardchecking-MRV-LCV
    start_time_fml = time.perf_counter()
    # FIX: don't forget to enable this when FML actually works
    # FML(sachovnica, velkost_sachovnice)
    elapsed_time_fml = time.perf_counter() - start_time_fml
    steps_taken_fml = len(kroky)

    # Výpis štatistík
    stats_message = (
        f"Algorithm: DFS\n"
        f"Time Taken: {elapsed_time_dfs:.6f} seconds\n"
        f"Steps Taken: {steps_taken_dfs}\n\n"
        f"Algorithm: Hill-Climbing\n"
        f"Time Taken: {elapsed_time_hc:.6f} seconds\n"
        f"Steps Taken: {steps_taken_hc}\n"
        f"Random Resets: {random_resety}\n"
        f"Algorithm: Forwardchecking-MRV-LCV\n"
        f"Time Taken: {elapsed_time_fml:.6f} seconds\n"
        f"Steps Taken: {steps_taken_fml}\n"
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
    elif algoritmus == "Forwardchecking-MRV-LCV":
        FML(sachovnica, velkost_sachovnice)
        display_steps(platno, root)
    elif algoritmus == "Show Stats":
        ukaz_staty(sachovnica, root)


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
        values=["DFS", "Hill-Climbing", "Forwardchecking-MRV-LCV", "Show Stats"],
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
