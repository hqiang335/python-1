import random

#常量
PLANT_REPRODUCE_CHANCE = 0.1
HERBIVORE_REPRODUCE_CHANCE = 0.15
CARNIVORE_REPRODUCE_CHANCE = 0.1

HERBIVORE_REPRODUCE_ENERGY = 20
CARNIVORE_REPRODUCE_ENERGY = 40

ORIGINAL_ENERGY_HERBIVORE = 15
ORIGINAL_ENERGY_CARNIVORE = 25
ORIGINAL_ENERGY_HERBIVORE_CHILD = 10
ORIGINAL_ENERGY_CARNIVORE_CHILD = 20

HERBIVORE_REPRODUCE_COST = 8
CARNIVORE_REPRODUCE_COST = 20

HERBIVORE_ENERGY_EAT_GAIN = 10
CARNIVORE_ENERGY_EAT_GAIN = 20



class Organism:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def update(self, ecosystem):
        pass


class Plant(Organism):
    def __init__(self, x, y, symbol = "🌳"):
        super().__init__(x, y, symbol)

    def update(self, ecosystem):
        random_chance = random.random()
        if random_chance < PLANT_REPRODUCE_CHANCE:
            empty_cells = ecosystem.get_adjacent_empty_cells(self.x, self.y)
            if empty_cells:
                new_x, new_y = random.choice(empty_cells)
                ecosystem.add_list.append(Plant(new_x, new_y))


class Animal(Organism):
    def __init__(self, x, y, symbol, energy):
        super().__init__(x, y, symbol)
        self.energy = energy

    def update(self, ecosystem):
        self.energy -= 1

    def move(self, ecosystem):
        empty_cells = ecosystem.get_adjacent_empty_cells(self.x, self.y)
        if empty_cells:
            new_x, new_y = random.choice(empty_cells)
            self.x = new_x
            self.y = new_y
   
class Herbivore(Animal):
    def __init__(self,x,y,symbol = "🐑",energy = ORIGINAL_ENERGY_HERBIVORE):
        super().__init__(x,y,symbol,energy)

    def update(self, ecosystem):
        super().update(ecosystem) 
        if self.energy <= 0:
            ecosystem.remove_list.append(self)
            return
            
        plant_target = ecosystem.get_adjacent_type(self.x, self.y, "🌳")
        #有吃则吃
        if plant_target: 
            target_organism = random.choice(plant_target)
            if not ecosystem.is_in_remove_list(target_organism): #防止“抢食重叠bug”出现，确保同一坐标只登记一次
                ecosystem.remove_list.append(target_organism)
                self.x = target_organism.x
                self.y = target_organism.y
                self.energy += HERBIVORE_ENERGY_EAT_GAIN
                return
        #繁殖 
        elif self.energy > HERBIVORE_REPRODUCE_ENERGY and random.random() < HERBIVORE_REPRODUCE_CHANCE:
            empty_cells = ecosystem.get_adjacent_empty_cells(self.x, self.y) 
            if empty_cells:
                new_x, new_y = random.choice(empty_cells)
                ecosystem.add_list.append(Herbivore(new_x, new_y, "🐑", ORIGINAL_ENERGY_HERBIVORE_CHILD))
                self.energy -= HERBIVORE_REPRODUCE_COST
                return
        #移动
        else:
            self.move(ecosystem)


class Carnivore(Animal):
    def __init__(self,x,y,symbol = "🐺",energy = ORIGINAL_ENERGY_CARNIVORE):
        super().__init__(x,y,symbol,energy)

    def update(self, ecosystem):
        super().update(ecosystem)
        if self.energy <= 0:
            ecosystem.remove_list.append(self)
            return
        
        hunt_target = ecosystem.get_adjacent_type(self.x, self.y, "🐑")
        if hunt_target: 
            target_organism = random.choice(hunt_target)
            if not ecosystem.is_in_remove_list(target_organism): #防止“抢食重叠bug”出现，确保同一坐标只登记一次
                ecosystem.remove_list.append(target_organism)
                self.x = target_organism.x
                self.y = target_organism.y
                self.energy += CARNIVORE_ENERGY_EAT_GAIN
                return
        elif self.energy > CARNIVORE_REPRODUCE_ENERGY and random.random() < CARNIVORE_REPRODUCE_CHANCE:
            empty_cells = ecosystem.get_adjacent_empty_cells(self.x, self.y)
            if empty_cells:
                new_x, new_y = random.choice(empty_cells)
                ecosystem.add_list.append(Carnivore(new_x, new_y, "🐺", ORIGINAL_ENERGY_CARNIVORE_CHILD))
                self.energy -= CARNIVORE_REPRODUCE_COST
                return
        else:
            self.move(ecosystem)
