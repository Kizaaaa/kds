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
    def __init__(self, x, y, energy=None):
        super().__init__(x, y)
        self.steps_since_reproduce = 0
        # Add energy system to prey
        self.energy = energy if energy is not None else random.randint(15, 25)  # Random starting energy
        self.max_energy = 30  # Maximum energy capacity

    def step(self, grid_size, reproduce_interval, occupied_positions, food_positions=None, energy_gain_from_food=5, energy_loss_per_step=1, min_reproduce_energy=15):
        # Move first
        self.move(grid_size)
        
        # Consume energy for movement
        self.energy -= energy_loss_per_step
        
        # Look for food (could be vegetation/plankton positions)
        if food_positions and (self.x, self.y) in food_positions:
            self.energy = min(self.max_energy, self.energy + energy_gain_from_food)
        else:
            # Natural foraging - prey can find some food even without specific food positions
            if random.random() < 0.3:  # 30% chance to find natural food
                self.energy = min(self.max_energy, self.energy + 2)
        
        self.steps_since_reproduce += 1
        
        # Check reproduction conditions: time interval, energy, and space
        if (self.steps_since_reproduce >= reproduce_interval and 
            self.energy >= min_reproduce_energy and 
            (self.x, self.y) not in occupied_positions):
            
            # Reproduction costs energy
            reproduction_cost = 8
            if self.energy >= reproduction_cost * 2:  # Need enough energy for both parent and child
                self.energy -= reproduction_cost
                child_energy = reproduction_cost
                self.steps_since_reproduce = 0
                return Prey(self.x, self.y, child_energy)
        
        return None
    
    def is_alive(self):
        """Check if prey is still alive (has energy)"""
        return self.energy > 0


class Predator(Agent):
    def __init__(self, x, y, energy):
        super().__init__(x, y)
        self.energy = energy
        self.steps_since_reproduce = 0

    def step(self, grid_size, prey_positions, energy_gain, energy_loss, reproduce_interval, occupied_positions, min_reproduce_energy=None):
        # Look for adjacent prey to hunt
        targets = [(x, y) for (x, y) in prey_positions if abs(x - self.x) + abs(y - self.y) == 1]
        if targets:
            # Move to prey position (hunting)
            self.x, self.y = random.choice(targets)
        else:
            # Regular movement when no prey nearby
            self.move(grid_size)

        # Energy management
        self.energy -= energy_loss
        self.steps_since_reproduce += 1
        ate_prey = (self.x, self.y) in prey_positions
        
        if ate_prey:
            self.energy += energy_gain

        # Reproduction logic
        min_energy_for_reproduction = min_reproduce_energy if min_reproduce_energy else energy_loss * 10
        
        if (self.steps_since_reproduce >= reproduce_interval and 
            self.energy > min_energy_for_reproduction and 
            (self.x, self.y) not in occupied_positions):
            
            # Split energy between parent and child
            child_energy = self.energy // 2
            self.energy = self.energy // 2
            self.steps_since_reproduce = 0
            return Predator(self.x, self.y, child_energy), ate_prey
            
        return None, ate_prey
    
    def is_alive(self):
        """Check if predator is still alive (has energy)"""
        return self.energy > 0


class Food:
    """Represents food sources (vegetation/plankton) that prey can consume"""
    def __init__(self, x, y, regeneration_time=10):
        self.x = x
        self.y = y
        self.available = True
        self.regeneration_time = regeneration_time
        self.time_until_regen = 0
    
    def consume(self):
        """Consume this food source"""
        if self.available:
            self.available = False
            self.time_until_regen = self.regeneration_time
            return True
        return False
    
    def step(self):
        """Update food regeneration"""
        if not self.available:
            self.time_until_regen -= 1
            if self.time_until_regen <= 0:
                self.available = True