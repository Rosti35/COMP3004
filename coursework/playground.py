import time
from simulation import *
from config import *


 
# Run a single simulation and return the runtime
def run_simulation(agent_type, num_agents, num_enemies, maze_size, dynamic_enemies):
    # Create and set up the simulation
    simulation = PrimMazeSimulation(800, 800, dynamic_enemies, False)
    simulation.new_simulation(agent_type, num_agents, num_enemies, maze_size)
    
    # Run the simulation and measure the time
    start_time = time.time()
    simulation.run()
    run_time = time.time() - start_time
    
    return run_time, simulation.get_moves()


# Main part of the code
agent_type = A_STAR_AGENT
DYNAMIC_ENEMIES = False
num_agents = 1
num_enemies = 30
maze_size = 10

run_simulation(agent_type, num_agents, num_enemies, maze_size, DYNAMIC_ENEMIES)