import pygame
import random
import numpy as np
import pickle
import time
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
STATS_WIDTH = 200
screen = pygame.display.set_mode((WIDTH + STATS_WIDTH, HEIGHT))
pygame.display.set_caption("Ecosystem Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Simulation parameters
NUM_FOOD = 50
NUM_ANIMALS = 15
NUM_PREDATORS = 8
MUTATION_RATE = 0.1  # Increased mutation rate for genetic algorithm
STATS_X_OFFSET = 800
FOOD_SPAWN_INTERVAL = 0.3
WATER_POOLS = [(100, 100), (400, 400), (700, 500)]

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 30

average_blue_speeds = []
average_blue_visions = []
average_blue_energies = []
average_blue_thirsts = []
average_number_of_blue_animals = []
average_brown_speeds = []
average_brown_visions = []
average_brown_energies = []
average_brown_thirsts = []
average_number_of_brown_animals = []

# Entities
class Food:
   def __init__(self):
      self.x = random.randint(0, WIDTH)
      self.y = random.randint(0, HEIGHT)

   def draw(self):
      pygame.draw.circle(screen, GREEN, (self.x, self.y), 5)

class Water:
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def draw(self):
      pygame.draw.circle(screen, LIGHT_BLUE, (self.x, self.y), 30)

class Animal:
   def __init__(self, species="blue", x=None, y=None, genes=None):
      if x is None and y is None:
         self.x = random.randint(0, WIDTH)
         self.y = random.randint(0, HEIGHT)
      else:
         self.x = x
         self.y = y
      if genes is None:
         self.genes = self.random_genes()
      else:
         self.genes = genes
      self.speed = self.decode_speed(self.genes)
      self.vision = self.decode_vision(self.genes)
      self.energy = 320  # initial energy
      self.direction = random.uniform(0, 2 * np.pi)
      self.direction_change_interval = random.randint(30, 60)
      self.direction_change_counter = 0
      self.thirst = 320
      self.species = species
      self.reproduction_threshold = 400  # initial reproduction threshold
      if species == "brown":
         self.speed *= 1.3
         self.vision *= 0.8
         self.reproduction_threshold = 300
      elif species == "blue":
         self.speed *= 0.8
         self.vision *= 1.3
         self.reproduction_threshold = 250 # bolje vide sporiji i brze se razmnozavaju

   def random_genes(self):
      return "".join(random.choice("01") for _ in range(16))

   def decode_speed(self, genes):
      return int(genes[:8], 2) / 255 * 20 

   def decode_vision(self, genes):
      return int(genes[8:], 2) / 255 * 250

   def crossover(self, parent=None):
      crossover_point = random.randint(0, 15)
      child_genes = self.genes[:crossover_point] + parent.genes[crossover_point:]
      return child_genes
   
   def mutate(self):
      genes_list = list(self.genes)
      for i in range(len(genes_list)):
         if random.random() < MUTATION_RATE:
            genes_list[i] = "0" if genes_list[i] == "1" else "1"
      self.genes = "".join(genes_list)
      self.speed = self.decode_speed(self.genes)
      self.vision = self.decode_vision(self.genes)

   def group_behavior(self, animals):
      group_center_x = 0
      group_center_y = 0
      group_count = 0
      for animal in animals:
         if animal != self and ((self.x - animal.x) ** 2 + (self.y - animal.y) ** 2) ** 0.5 < self.vision:
            group_center_x += animal.x
            group_center_y += animal.y
            group_count += 1
      if group_count > 0:
         group_center_x /= group_count
         group_center_y /= group_count
         self.x += (group_center_x - self.x) * 0.05
         self.y += (group_center_y - self.y) * 0.05

   def move(self):
      if self.thirst < 100:
         nearest_water = self.find_nearest_water(WATER_POOLS)
         if nearest_water:
            water_dx = nearest_water[0] - self.x
            water_dy = nearest_water[1] - self.y
            distance = (water_dx ** 2 + water_dy ** 2) ** 0.5
            if distance < self.vision:
               self.x += self.speed * water_dx / distance
               self.y += self.speed * water_dy / distance
            else:
               self.random_move()
         else:
            self.random_move()
      elif self.energy >= 250:
         nearest_animal = self.find_nearest_animal(animals)
         if nearest_animal:
            animal_dx = nearest_animal.x - self.x
            animal_dy = nearest_animal.y - self.y
            distance = (animal_dx ** 2 + animal_dy ** 2) ** 0.5
            if distance == 0 or distance > self.vision:
               self.random_move()
            else:
               self.x += self.speed * animal_dx / distance
               self.y += self.speed * animal_dy / distance
         else:
            self.random_move()
      elif self.energy < 150:
         nearest_food = self.find_nearest_food(food_list)
         if nearest_food:
            food_dx = nearest_food.x - self.x
            food_dy = nearest_food.y - self.y
            distance = (food_dx ** 2 + food_dy ** 2) ** 0.5
            if distance < self.vision:
               self.x += self.speed * food_dx / distance
               self.y += self.speed * food_dy / distance
            else:
               self.random_move()
         else:
            self.random_move()
      else:
         if self.species == "blue":
            self.group_behavior(animals)
         else:
            self.random_move()
      if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
         self.x = max(0, min(WIDTH, self.x))
         self.y = max(0, min(HEIGHT, self.y))
      self.energy -= 1 + (self.speed / 20) 
      self.thirst -= 1 + (self.speed / 20) 
      # self.energy -= 1 
      # self.thirst -= 1  

   def random_move(self):
      if self.direction_change_counter >= self.direction_change_interval:
         self.direction = random.uniform(0, 2 * np.pi)
         self.direction_change_counter = 0
         self.direction_change_interval = random.randint(30, 60)
      
      self.x += self.speed * np.cos(self.direction)
      self.y += self.speed * np.sin(self.direction)
      self.direction_change_counter += 1

   def find_nearest_food(self, food_list):
      nearest = None
      min_distance = self.vision
      for food in food_list:
         distance = ((self.x - food.x) ** 2 + (self.y - food.y) ** 2) ** 0.5
         if distance < min_distance:
               nearest = food
               min_distance = distance
      return nearest
   
   def find_nearest_animal(self, animals):
      nearest = None
      min_distance = self.vision
      for animal in animals:
         distance = ((self.x - animal.x) ** 2 + (self.y - animal.y) ** 2) ** 0.5
         if distance < min_distance and animal != self:
               nearest = animal
               min_distance = distance
      return nearest
   
   def fitness(self):
      return self.vision + self.speed 

   def find_nearest_water(self, water_pools):
      nearest = None
      min_distance = self.vision
      for water in water_pools:
         distance = ((self.x - water[0]) ** 2 + (self.y - water[1]) ** 2) ** 0.5
         if distance < min_distance:
               nearest = water
               min_distance = distance
      return nearest

   def drink(self, water_pools):
      if self.thirst < 200:
         nearest_water = self.find_nearest_water(water_pools)
         if nearest_water:
            water_dx = nearest_water[0] - self.x
            water_dy = nearest_water[1] - self.y
            distance = (water_dx ** 2 + water_dy ** 2) ** 0.5
            if distance < 10:
               self.thirst += 300  # Increased thirst gain from drinking

   def draw(self):
      color = BROWN if self.species == "brown" else BLUE
      pygame.draw.circle(screen, color, (self.x, self.y), 8)

   def eat(self, food_list):
      if self.energy < 200:  # Only eat when energy is low you dont have to starve to eat
         nearest_food = self.find_nearest_food(food_list)
         if nearest_food and abs(self.x - nearest_food.x) < 10 and abs(self.y - nearest_food.y) < 10:
               food_list.remove(nearest_food)
               self.energy += 200  # Increased energy gain from eating

   def reproduce(self, animals):
      if self.energy > self.reproduction_threshold:  # Lowered reproduction threshold
         nearest_animal = self.find_nearest_animal(animals)
         if nearest_animal and abs(self.x - nearest_animal.x) < 15 and abs(self.y - nearest_animal.y) < 15 and nearest_animal.energy > 250:
            self.energy /= 2
            nearest_animal.energy /= 2
            child_genes = self.crossover(nearest_animal)
            child_species = random.choice([self.species, nearest_animal.species])
            child = Animal(child_species, self.x, self.y, genes=child_genes)
            child.mutate()
            animals.append(child)

def calculate_averages():
   blue_animals = [animal for animal in animals if animal.species == "blue"]
   brown_animals = [animal for animal in animals if animal.species == "brown"]

   def calculate_species_averages(species_animals):
      if species_animals:
         avg_speed = sum(animal.speed for animal in species_animals) / len(species_animals)
         avg_vision = sum(animal.vision for animal in species_animals) / len(species_animals)
         avg_energy = sum(animal.energy for animal in species_animals) / len(species_animals)
         avg_thirst = sum(animal.thirst for animal in species_animals) / len(species_animals)
      else:
         avg_speed = avg_vision = avg_energy = avg_thirst = 0
      return avg_speed, avg_vision, avg_energy, avg_thirst

   blue_averages = calculate_species_averages(blue_animals)
   brown_averages = calculate_species_averages(brown_animals)

   return blue_averages, brown_averages

# Simulation setup
def reset_simulation():
   global food_list, animals, start_time, last_food_spawn_time
   food_list = [Food() for _ in range(NUM_FOOD)]
   animals = [Animal(species="blue") for _ in range(NUM_ANIMALS // 2)] + \
             [Animal(species="brown") for _ in range(NUM_ANIMALS // 2)]
   start_time = time.time()
   last_food_spawn_time = start_time

def save_population():
   with open('population.pkl', 'wb') as f:
      pickle.dump((animals, food_list), f)

def load_population():
   global food_list, animals
   try:
      with open('population.pkl', 'rb') as f:
         animals, food_list = pickle.load(f)
      if not animals:
         reset_simulation()
   except FileNotFoundError:
      reset_simulation()

load_population()

# Main loop
start_time = time.time()
last_food_spawn_time = start_time   
running = True
while running:
   screen.fill(WHITE)

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False

   # Draw and update food
   for food in food_list:
      food.draw()

   for water in WATER_POOLS:
      Water(water[0], water[1]).draw()

   # Update and draw animals
   for animal in animals[:]:
      animal.move()
      animal.eat(food_list)
      animal.drink(WATER_POOLS)
      animal.reproduce(animals)
      animal.draw()
      if animal.energy <= 0 or animal.thirst <= 0:
         animals.remove(animal)

   blue_averages, brown_averages = calculate_averages()
   avg_blue_speed, avg_blue_vision, avg_blue_energy, avg_blue_thirst = blue_averages
   avg_brown_speed, avg_brown_vision, avg_brown_energy, avg_brown_thirst = brown_averages
   average_blue_speeds.append(avg_blue_speed)
   average_blue_visions.append(avg_blue_vision)
   average_blue_energies.append(avg_blue_energy)
   average_blue_thirsts.append(avg_blue_thirst)
   average_number_of_blue_animals.append(len([animal for animal in animals if animal.species == "blue"]))
   average_brown_speeds.append(avg_brown_speed)
   average_brown_visions.append(avg_brown_vision)
   average_brown_energies.append(avg_brown_energy)
   average_brown_thirsts.append(avg_brown_thirst)
   average_number_of_brown_animals.append(len([animal for animal in animals if animal.species == "brown"]))

   font = pygame.font.SysFont(None, 24)
   stats_surface = pygame.Surface((STATS_WIDTH, HEIGHT))
   stats_surface.fill(WHITE)

   stats_text = [
      f"Blue Speed: {avg_blue_speed:.2f}",
      f"Blue Vision: {avg_blue_vision:.2f}",
      f"Blue Energy: {avg_blue_energy:.2f}",
      f"Blue Thirst: {avg_blue_thirst:.2f}",
      f"Brown Speed: {avg_brown_speed:.2f}",
      f"Brown Vision: {avg_brown_vision:.2f}",
      f"Brown Energy: {avg_brown_energy:.2f}",
      f"Brown Thirst: {avg_brown_thirst:.2f}",
      f"Animal count: {len(animals)}",
      f"blue Animals count: {len([animal for animal in animals if animal.species == 'blue'])}",
      f"Brown Animals count: {len([animal for animal in animals if animal.species == 'brown'])}",
   ]

   for i, line in enumerate(stats_text):
      text_surface = font.render(line, True, BLACK)
      stats_surface.blit(text_surface, (10, 10 + i * 30))

   screen.blit(stats_surface, (STATS_X_OFFSET, 0))

   pygame.display.flip()
   clock.tick(FPS)

   if time.time() - last_food_spawn_time > FOOD_SPAWN_INTERVAL:
      food_list.append(Food())
      last_food_spawn_time = time.time()

   # Check if 20 seconds have passed or all animals are dead
   if time.time() - start_time > 10080 or not animals: #or not predators:
      save_population()
      reset_simulation()
      running = False

pygame.quit()
save_population()


# Plotting speed, vision, energy, thirst, and number of animals over time
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(average_blue_speeds, label='Average Speed')
plt.xlabel('Time (frames)')
plt.ylabel('Average Speed')
plt.title('Average Speed over Time')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(average_blue_visions, label='Average Vision')
plt.xlabel('Time (frames)')
plt.ylabel('Average Vision')
plt.title('Average Vision over Time')
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(average_blue_energies, label='Average Energy')
plt.plot(average_blue_thirsts, label='Average Thirst')
plt.xlabel('Time (frames)')
plt.ylabel('Average Value')
plt.title('Average Energy and Thirst over Time')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(average_number_of_blue_animals, label='Number of Animals')
plt.xlabel('Time (frames)')
plt.ylabel('Number of Animals')
plt.title('Number of Animals over Time')
plt.legend()

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(average_brown_speeds, label='Average Speed')
plt.xlabel('Time (frames)')
plt.ylabel('Average Speed')
plt.title('Average Speed over Time')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(average_brown_visions, label='Average Vision')
plt.xlabel('Time (frames)')
plt.ylabel('Average Vision')
plt.title('Average Vision over Time')
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(average_brown_energies, label='Average Energy')
plt.plot(average_brown_thirsts, label='Average Thirst')
plt.xlabel('Time (frames)')
plt.ylabel('Average Value')
plt.title('Average Energy and Thirst over Time')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(average_number_of_brown_animals, label='Number of Animals')
plt.xlabel('Time (frames)')
plt.ylabel('Number of Animals')
plt.title('Number of Animals over Time')
plt.legend()

plt.tight_layout()
plt.show()