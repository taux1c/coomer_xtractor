
from json import dumps, loads
from pathlib import Path
import webbrowser


from coomer_xtractor.config import profiles_folder


class User:

    def __init__(self):
        self.index = 0
        self.display_name = None
        self.favorite_urls = None
        self.save_location = None
        self.db_string = None
        self.max_concurrent_downloads = 10
        self.max_concurrent_requests = 10


    def build(self):
        self.display_name = input("What can we call you?: ")
        self.favorite_urls = input("What models do you want to follow? Enter the full url of the main model page. (Separate with comma.): \n").split(',')
        self.save_location = Path(input("Where do you want to save your data?: "))
        while True:
            self.max_concurrent_downloads = int(input("How many concurrent downloads do you want to make? (Default is 10): "))
            if type(self.max_concurrent_downloads) == int and self.max_concurrent_downloads > 0:
                break
            else:
                print("Please enter a number greater than 0.")
        while True:
            self.max_concurrent_requests = int(input("How many concurrent requests do you want to make? (Default is 10): "))
            if type(self.max_concurrent_requests) == int and self.max_concurrent_requests > 0:
                break
            else:
                print("Please enter a number greater than 0.")

        self.db_string = f"sqlite:///{self.save_location}/{self.display_name}_posts.db"
        self.save()

    def save(self):
        profile_name = f"{self.display_name}.json"
        self.save_location.mkdir(parents=True, exist_ok=True)
        self.save_location = str(self.save_location)
        self.favorite_urls = dumps(self.favorite_urls)
        with open(Path(profiles_folder) / profile_name, 'w') as f:
            f.write(dumps(self.__dict__, indent=6))

    def load(self, profile_name):
        with open(Path(profiles_folder) / profile_name, 'r') as f:
            self.__dict__ = loads(f.read())
            self.save_location = Path(self.save_location)
            self.favorite_urls = loads(self.favorite_urls)

    def __repr__(self):
        return f"display_name={self.display_name}, categories={self.categories}, save_location={self.save_location}"

    def set_max_concurrent_requests(self):
        self.max_concurrent_requests = int(input("How many concurrent requests do you want to make? (Default is 10): "))
        self.save()


def select_profile():
    if not Path(profiles_folder).exists():
        Path(profiles_folder).mkdir(parents=True, exist_ok=True)
    profiles = [profile for profile in Path(profiles_folder).iterdir() if profile.is_file() and profile.exists()]
    if len(profiles) == 0:
        print("No profiles found. Please create one.")
        quit()
    print("Select a profile:")
    for i, profile in enumerate(profiles):
        print(f"{i+1}. {profile.stem}")
    profile_selection = int(input("Enter the number of the profile you want to use: "))
    profile = profiles[profile_selection-1]
    p = User()
    p.load(profile.name)
    return p


async def create_profile():
    p = User()
    p.build()

async def edit_profile():
    p = select_profile()
    p.build()

async def delete_profile():
    p = select_profile()
    Path(profiles_folder, f"{p.display_name}.json").unlink()
    print(f"Deleted {p.display_name}.")

def start():
    try:
        webbrowser.open("https://www.buymeacoffee.com/taux1c")
    except:
        print("Please consider supporting the developer by visiting https://www.buymeacoffee.com/taux1c")