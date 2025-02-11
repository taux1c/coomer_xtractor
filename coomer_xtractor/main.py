
from asyncio import run
import cowsay


from coomer_xtractor.menus.main_menu import main_menu






def main():
    print(cowsay.dragon('COOMER XTRACTOR - Slow Burn'))
    run(main_menu())



if __name__ == "__main__":
    main()