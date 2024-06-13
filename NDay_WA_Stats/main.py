import requests
import time
import sys
import xml.etree.ElementTree as ET
import dotenv
from dotenv import env

dotenv.load_dotenv("./env")

headers = {
    "User-Agent": env("USER_AGENT")
}

def format_nations(nations):
    """
    Formats a list of nation names by removing the pretitle and the word "of" from each name.

    Args:
        nations (list): A list of nation names.

    Returns:
        list: A list of formatted nation names.
    """
    formatted_nations = []
    for nation in nations:
        index = nation.find(" of ") # Find the index of the word " of " in the nation name, since each nation name is formatted as "Pretitle of Nation"
        if index != -1:
            formatted_nations.append(nation[index + 4:]) # Append the nation name without the pretitle and the word " of "
        else:
            formatted_nations.append(nation)
    # Remove the last character of each element in formatted_nations
    # formatted_nations = [nation[:-1] for nation in formatted_nations]

    print(f"Parsed {len(formatted_nations)} nations from the file. Expected time to fully parse: {(((len(formatted_nations) / 50) * 32) + (len(formatted_nations) / 50) * 30) / 60} minutes.")
    return formatted_nations

def filter_away_nonwa_nations(formatted_nations, nations_errors, faction):
    """
    Filters away the non-WA nations from the list of nations.

    Returns:
        list: The list of WA nations.
    """
    wa_nations = []
    estimated_remaining_time_in_seconds = ((len(formatted_nations) / 50) * 32) + (len(formatted_nations) / 50) * 30
    i = 0
    for nation in formatted_nations:
        url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation[:-1]}&q=wa"
        try:
            print(f"Checking nation {nation[:-1]}...")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                if root.find("UNSTATUS").text != "Non-member":
                    wa_nations.append(nation)
                    print(f"WA nation found: {nation[:-1]}")
        except requests.exceptions.HTTPError:
            print(f"Error: {response.status_code} and nation == {nation[:-1]}")
            nations_errors.write(nation + "\n")
            pass
        i += 1
        if (i == 47):
            estimated_remaining_time_in_seconds = estimated_remaining_time_in_seconds - 47  / 50 * 32 - 47 / 50 * 30
            print(f"API rate limit reached, sleeping for 32 seconds. The estimated remaining time is {(estimated_remaining_time_in_seconds + 32) / 60} minutes.")
            time.sleep(32)
            i = 0
    print(f"I have found {len(wa_nations)} WA nations in {faction}. Now proceeding to sort them by specialities... Estimated time to fully parse: {len(wa_nations) / 60} minutes.")
    return wa_nations

def sort_by_speciality(wa_nations, faction):
    """
    Sorts a list of nations by their speciality and returns separate lists for each speciality.

    Args:
        wa_nations (list): A list of nations, where each nation is represented as a string.

    Returns:
        tuple: A tuple containing four lists: mils_nations, strats_nations, econs_nations, intels_nations.
            - mils_nations (list): A list of nations with military speciality.
            - strats_nations (list): A list of nations with strategic speciality.
            - econs_nations (list): A list of nations with economic speciality.
            - intels_nations (list): A list of nations with intelligence speciality.
    """
    mils, strats, econs, intels = 0, 0, 0, 0
    mils_nations = []
    strats_nations = []
    econs_nations = []
    intels_nations = []
    for nation in wa_nations:
        if nation[-1] == "S":
            print(f"{nation} is a Strategic Specialist.")
            strats += 1
            strats_nations.append(nation[:-1])
        elif nation[-1] == "M":
            print(f"{nation} is a Military Specialist.")
            mils += 1
            mils_nations.append(nation[:-1])
        elif nation[-1] == "E":
            print(f"{nation} is an Economic Specialist.")
            econs += 1
            econs_nations.append(nation[:-1])
        elif nation[-1] == "I":
            print(f"{nation} is an Intel Specialist.")
            intels += 1
            intels_nations.append(nation[:-1])
    print(f"===== {faction} STATS =====\nNumber of Military Specialists: {len(mils_nations)}\nNumber of Economic Specialists: {len(econs_nations)}\nNumber of Strategic Specialists: {len(strats_nations)}\nNumber of Intel Specialists: {len(intels_nations)}\n")
    return mils_nations, strats_nations, econs_nations, intels_nations

def open_files(faction):
    faction_file = open(f"./{faction}.txt")
    nations = faction_file.read().splitlines()
    nations_errors = open(f"./{faction}_errors.txt", "w")
    faction_file.close
    return nations, nations_errors

def write_to_speciality_files(nations, faction, speciality):
    speciality_file = open(f"./{faction}_{speciality}.txt", "w")
    for nation in nations:
        speciality_file.write(nation + "\n")
    speciality_file.close()

def main():
    faction = sys.argv[1]
    nations, nations_errors = open_files(faction)
    formatted_nations = format_nations(nations)
    wa_nations = filter_away_nonwa_nations(formatted_nations, nations_errors, faction)
    mils_nations, strats_nations, econs_nations, intels_nations = sort_by_speciality(wa_nations, faction)

    write_to_speciality_files(mils_nations, faction, "S")
    write_to_speciality_files(strats_nations, faction, "M")
    write_to_speciality_files(econs_nations, faction, "E")
    write_to_speciality_files(intels_nations, faction, "I")

    nations_errors.close()


if __name__ == "__main__":
    main()