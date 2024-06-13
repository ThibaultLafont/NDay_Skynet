import sys

def process_file(faction, category):
    with open(f"./{faction}_{category}.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        line = line.replace(" ", "_")
        with open(f"./{faction}/{faction}_{category}_URLs.txt", "a") as f:
            f.write(f"https://www.nationstates.net/nation={line}/page=nukes/view=incoming\n")

def main():
    faction = sys.argv[1]
    print(f"Making URLs for {faction}...")
    categories = ['E', 'M', 'S', 'I']
    for category in categories:
        process_file(faction, category)

if __name__ == "__main__":
    main()