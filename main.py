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
            print("请输入一个正整数！")

def main():
    grid = get_int("请输入网格大小：")
    n_plant = get_int("请输入初始植物数量：")
    n_herb = get_int("请输入初始食草动物数量：")
    n_carn = get_int("请输入初始食肉动物数量：")
    ticks = get_int("请输入模拟总时长（tick 数）：")

    if n_plant + n_herb + n_carn > grid * grid:
        print("错误：生物数量超过网格容量！")
        return

    eco = Ecosystem(grid, n_plant, n_herb, n_carn)
    eco.run(ticks)

if __name__ == "__main__":
    main()
