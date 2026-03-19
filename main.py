import sys

sys.path.append('./game')
sys.path.append('./globalvariables')
sys.path.append('./Menus')
sys.path.append('./units')
sys.path.append('./players')
sys.path.append('./enemies')
sys.path.append('./abilities')
sys.path.append('./encounter')

from game import game

def main():
    game()


if __name__ == "__main__":
    main()
