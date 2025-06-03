import random

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, grid_size):
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.x = (self.x + dx) % grid_size
        self.y = (self.y + dy) % grid_size


class Prey(Agent):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.steps_since_reproduce = 0

    def step(self, grid_size, reproduce_interval, occupied_positions):
        self.move(grid_size)
        self.steps_since_reproduce += 1
        if self.steps_since_reproduce >= reproduce_interval:
            if (self.x, self.y) not in occupied_positions:
                self.steps_since_reproduce = 0
                return Prey(self.x, self.y)
        return None


class Predator(Agent):
    def __init__(self, x, y, energy):
        super().__init__(x, y)
        self.energy = energy
        self.steps_since_reproduce = 0

    def step(self, grid_size, prey_positions, energy_gain, energy_loss, reproduce_interval, occupied_positions):
        targets = [(x, y) for (x, y) in prey_positions if abs(x - self.x) + abs(y - self.y) == 1]
        if targets:
            self.x, self.y = random.choice(targets)
        else:
            self.move(grid_size)

        self.energy -= energy_loss
        self.steps_since_reproduce += 1
        ate_prey = (self.x, self.y) in prey_positions
        if ate_prey:
            self.energy += energy_gain

        if self.steps_since_reproduce >= reproduce_interval and self.energy > energy_loss:
            if (self.x, self.y) not in occupied_positions:
                self.energy //= 2
                self.steps_since_reproduce = 0
                return Predator(self.x, self.y, self.energy), ate_prey
        return None, ate_prey
