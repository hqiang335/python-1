# main.py
from ecosystem import Ecosystem

def get_int(prompt):
    while True:
        try:
            val = int(input(prompt))
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("Please enter a positive integer!")

def main():
    grid = get_int("Enter n for n*n grid:")
    n_plant = get_int("Enter initial number of Plants🌳:")
    n_herb = get_int("Enter initial number of Herbivores🐑:")
    n_carn = get_int("Enter initial number of Carnivores🐺:")
    ticks = get_int("Enter total number of running ticks:")

    if n_plant + n_herb + n_carn > grid * grid:
        print("Error: The number of organisms exceeds the grid capacity!")
        return

    eco = Ecosystem(grid, n_plant, n_herb, n_carn)
    eco.run(ticks)

if __name__ == "__main__":
    main()
