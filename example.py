import simpy
import random

class World:
    def __init__(self, env):
        self.env = env
        self.prey_population = 100
        self.predator_population = 20
        self.prey = simpy.Resource(env, capacity=self.prey_population)
        self.predator = simpy.Resource(env, capacity=self.predator_population)
        self.duration = 50  # Czas trwania symulacji w sekundach

def prey_behaviour(env, world):
    while env.now < world.duration:
        yield env.timeout(1)
        if random.random() < 0.1:  # Szansa na reprodukcję ofiary
            world.prey_population += 10

def predator_behaviour(env, world):
    while env.now < world.duration:
        yield env.timeout(1)
        if random.random() < 0.2:  # Szansa na reprodukcję drapieżnika
            world.predator_population += 5
        if random.random() < 0.2 and world.prey_population > 0:  # Szansa na polowanie
            world.prey_population -= 1

def run_simulation(env, world):
    prey_process = env.process(prey_behaviour(env, world))
    predator_process = env.process(predator_behaviour(env, world))
    yield env.timeout(world.duration)  # Czas trwania symulacji

env = simpy.Environment()
world = World(env)
env.process(run_simulation(env, world))
env.run()

print("Populacja ofiar:", world.prey_population)
print("Populacja drapieżników:", world.predator_population)