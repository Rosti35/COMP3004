import time
import matplotlib.pyplot as plt
from simulation import *
import matplotlib
from config import *

# Run a single simulation and return the runtime and number of moves
def run_simulation(agent_type, num_agents, num_enemies, maze_size):
    # Create and set up the simulation
    simulation = PrimMazeSimulation(800, 800, DYNAMIC_ENEMIES)
    simulation.new_simulation(agent_type, num_agents, num_enemies, maze_size)

    # Run the simulation and measure the time and number of moves
    start_time = time.time()
    simulation.run()
    run_time = time.time() - start_time
    moves = simulation.get_moves()

    return run_time, moves

# Run multiple simulations and return a list of runtimes and number of moves
def run_simulations(num_runs, agent_type, num_agents, num_enemies, maze_size):
    runtimes = []
    moves = []
    # Run the simulation multiple times and store the runtimes and number of moves
    for i in range(num_runs):
        run_time, num_moves = run_simulation(agent_type, num_agents, num_enemies, maze_size)
        runtimes.append(run_time)
        moves.append(num_moves)
        print(f"Run {i + 1}: {run_time:.2f} seconds; {num_moves} moves")

    return runtimes, moves

# Calculate the average
def calculate_average(data):
    return sum(data) / len(data)

# Plot runtimes and number of moves along with the average runtime and average number of moves
def plot_runtimes_and_moves(runtimes, moves, average_runtime, average_moves, title):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(range(1, len(runtimes) + 1), runtimes, marker='o')
    ax1.set_xlabel("Run Number")
    ax1.set_ylabel("Runtime (seconds)")
    ax1.set_title("Simulation Runtimes")
    ax1.axhline(average_runtime, color='r', linestyle='--', label=f"Average: {average_runtime:.2f}s")
    ax1.legend()

    ax2.plot(range(1, len(moves) + 1), moves, marker='o')
    ax2.set_xlabel("Run Number")
    ax2.set_ylabel("Number of Moves")
    ax2.set_title("Simulation Moves")
    ax2.axhline(average_moves, color='r', linestyle='--', label=f"Average: {average_moves:.2f}")
    ax2.legend()

    fig.suptitle(title)
    plt.show()

# Main part of the code
agent_type = Q_TABLE_AGENT
DYNAMIC_ENEMIES = False
num_agents = 1
num_enemies = 10
maze_size = 20
num_runs = 10

# Run the simulations and calculate the average runtime and average number of moves
runtimes, moves = run_simulations(num_runs, agent_type, num_agents, num_enemies, maze_size)
average_runtime = calculate_average(runtimes)
average_moves = calculate_average(moves)
print(f"Agent type: {agent_type}, num_agents: {num_agents}, num_enemies: {num_enemies}, maze_size: {maze_size}")
print(f"Average runtime: {average_runtime:.2f} seconds")
print(f"Average number of moves: {average_moves:.2f}")

# Plot the runtime and number of moves data
title = f"Simulation Results (Agent type: Q_TABLE_AGENT, Maze type: Prim's Maze, num_enemies: {num_enemies}, maze_size: {maze_size})"
plot_runtimes_and_moves(runtimes, moves, average_runtime, average_moves, title)
