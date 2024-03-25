import simpy
import random

# Parametry początkowe
INITIAL_PREY_POPULATION = 100
INITIAL_PREDATOR_POPULATION = 20
SIMULATION_DURATION = 100
PREY_REPRODUCTION_RATE = 0.1
PREDATOR_REPRODUCTION_RATE = 0.05
PREDATION_RATE = 0.3

# Klasa reprezentująca środowisko
class Habitat:
    def __init__(self, env):
        self.env = env
        self.prey_population = INITIAL_PREY_POPULATION
        self.predator_population = INITIAL_PREDATOR_POPULATION

# Proces zachowania ofiar
def prey_behavior(env, habitat):
    while True:
        # Rozmnażanie się ofiar
        habitat.prey_population += PREY_REPRODUCTION_RATE * habitat.prey_population
        yield env.timeout(1)
        print(f"Ofiary: {habitat.prey_population:.2f} w czasie {env.now}")

# Proces zachowania drapieżników
def predator_behavior(env, habitat):
    while True:
        # Polowanie na ofiary
        prey_available = min(habitat.prey_population, PREDATION_RATE * habitat.predator_population)
        prey_consumed = random.uniform(0, prey_available)
        habitat.prey_population -= prey_consumed
        habitat.predator_population += PREDATOR_REPRODUCTION_RATE * prey_consumed
        yield env.timeout(1)
        print(f"Drapieżniki: {habitat.predator_population:.2f} w czasie {env.now}")

# Proces uruchamiający symulację
def run_simulation():
    env = simpy.Environment()
    habitat = Habitat(env)
    env.process(prey_behavior(env, habitat))
    env.process(predator_behavior(env, habitat))
    env.run(until=SIMULATION_DURATION)

if __name__ == "__main__":
    run_simulation()