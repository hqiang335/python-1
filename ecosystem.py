# ecosystem.py
from typing import Any


import random
import time
from organisms import Plant, Herbivore, Carnivore

class Ecosystem:
    def __init__(self, grid_size, n_plants, n_herbivores, n_carnivores):
        self.grid_size = grid_size
        self.tick = 0
        self.add_list = []
        self.remove_list = []
        self.organisms = []
        self.n_plants = n_plants
        self.n_herbivores = n_herbivores
        self.n_carnivores = n_carnivores

    def initialize(self, n_plants, n_herbivores, n_carnivores): #输入的动物或植物太多超过格子数？
        coords = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        random.shuffle(coords)
        for i in range(n_plants):
            x, y = coords.pop()
            self.organisms.append(Plant(x, y))
        for i in range(n_herbivores):
            x, y = coords.pop()
            self.organisms.append(Herbivore(x, y))
        for i in range(n_carnivores):
            x, y = coords.pop()
            self.organisms.append(Carnivore(x, y))

    def run(self, total_ticks):
        random.seed(42)#临时debug专用种子
        self.initialize(self.n_plants, self.n_herbivores, self.n_carnivores)
        print(f"Initialization:")
        grid = [['. ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for organism in self.organisms:
            grid[organism.x][organism.y] = organism.symbol
        for row in grid:
            print(" ".join(row))
        # self.display()
        for tick in range(total_ticks):
            self.tick = tick
            random.shuffle(self.organisms)
            for organism in self.organisms:
                organism.update(self)

            for remove_organism in self.remove_list:#去重？？？
                print(f"tick {tick} remove_organism: {remove_organism.symbol} at ({remove_organism.x}, {remove_organism.y})")
                # self.organisms.remove(remove_organism)
                if remove_organism in self.organisms:
                    self.organisms.remove(remove_organism)
                else:
                    print(f"警告: 找不到要移除的生物 {remove_organism.symbol} at ({remove_organism.x}, {remove_organism.y})")
            for add_organism in self.add_list:
                self.organisms.append(add_organism)
            self.remove_list = []
            self.add_list = []
            self.display()
            time.sleep(0.2)

    
    def display(self):
        print(f"--------------Tick {self.tick}---------------")
        grid = [['. ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for organism in self.organisms:
            grid[organism.x][organism.y] = organism.symbol
        for row in grid:
            print(" ".join(row))

    def get_organism_at(self, x, y):
        #获取指定坐标处的生物对象（如果有的话），否则返回None
        for organism in self.organisms:
            if organism.x == x and organism.y == y:
                return organism
        return None

    def get_adjacent_empty_cells(self,x, y):
        #获取指定坐标周围8个方向的空单元格（不包括自身）
        check = [-1,0,1]
        empty_cells = []
        for dx in check:
            for dy in check:
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if self.get_organism_at(nx, ny) is None:
                        empty_cells.append((nx, ny))
        return empty_cells

    def get_adjacent_type(self,x, y,type):
        #获取指定坐标周围8个方向的指定类型的生物单元格（不包括自身）
        check = [-1,0,1]
        query = []
        for dx in check:
            for dy in check:
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    organism = self.get_organism_at(nx, ny)
                    if organism is not None and organism.symbol == type:
                        query.append(organism)  # 返回生物对象而不是坐标
        return query

