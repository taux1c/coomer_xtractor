


from coomer_xtractor.actions.jobs import scrape_url, scrape_favorites
from coomer_xtractor.models.profiles import create_profile, edit_profile, delete_profile
from coomer_xtractor.models.profiles import start

async def close_program():
    start()
    quit()





async def main_menu():
    start()
    selections = {
        1: scrape_url,
        2: scrape_favorites,
        3: create_profile,
        4: edit_profile,
        5: delete_profile,
        6: close_program
    }
    while True:
        for k,v in selections.items():
            print(f"{k}: {v.__name__}")
        try:
            selection = int(input("Enter a number: "))
            if selection in selections.keys():
                await selections[selection]()
            else:
                print("Invalid selection.")
        except Exception as e:
            print(e)