import sys

def main():
    faction = sys.argv[1]
    print(f"Making URLs for {faction}...")
    with open(f"./{faction}_E.txt", "r") as f:
        econs = f.readlines()
    with open(f"./{faction}_M.txt", "r") as f:
        mils = f.readlines()
    with open(f"./{faction}_S.txt", "r") as f:
        strats = f.readlines()
    with open(f"./{faction}_I.txt", "r") as f:
        intels = f.readlines()
    for econ in econs:
        econ = econ[:-1]
        econ = econ.replace(" ", "_")
        with open(f"./{faction}/{faction}_E_URLs.txt", "a") as f:
            f.write(f"https://www.nationstates.net/nation={econ}/page=nukes/view=incoming\n")
    for mil in mils:
        mil = mil[:-1]
        mil = mil.replace(" ", "_")
        with open(f"./{faction}/{faction}_M_URLs.txt", "a") as f:
            f.write(f"https://www.nationstates.net/nation={mil}/page=nukes/view=incoming\n")
    for strat in strats:
        strat = strat[:-1]
        strat = strat.replace(" ", "_")
        with open(f"./{faction}/{faction}_S_URLs.txt", "a") as f:
            f.write(f"https://www.nationstates.net/nation={strat}/page=nukes/view=incoming\n")
    for intel in intels:
        intel = intel[:-1]
        intel = intel.replace(" ", "_")
        with open(f"./{faction}/{faction}_I_URLs.txt", "a") as f:
            f.write(f"https://www.nationstates.net/nation={intel}/page=nukes/view=incoming\n")

if __name__ == "__main__":
    main()