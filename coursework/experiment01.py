import time
import matplotlib.pyplot as plt
from simulation import *
import matplotlib
from config import *


# Run a single simulation and return the runtime
def run_simulation(agent_type, num_agents, num_enemies, maze_size):
    # Create and set up the simulation
    simulation = PrimMazeSimulation(800, 800, DYNAMIC_ENEMIES)
    simulation.new_simulation(agent_type, num_agents, num_enemies, maze_size)
    
    # Run the simulation and measure the time
    start_time = time.time()
    simulation.run()
    run_time = time.time() - start_time
    
    return run_time, simulation.get_moves()

# Run multiple simulations and return a list of runtimes
def run_simulations(num_runs, agent_type, num_agents, num_enemies, maze_size):
    runtimes = []
    moves_l = []
    # Run the simulation multiple times and store the runtimes
    for i in range(num_runs):
        run_time, moves = run_simulation(agent_type, num_agents, num_enemies, maze_size)
        runtimes.append(run_time)
        moves_l.append(moves)
        print(f"Run {i + 1}: {run_time:.2f} seconds; {moves} moves")
    
    return runtimes, moves_l

# Calculate the average
def calculate_average(data):
    return sum(data) / len(data)



# Run simulations for a specific agent type and store the average runtimes and average moves in 2D arrays
def run_agent_type_simulations(agent_type, num_agents, num_enemies_list, maze_sizes, num_runs):
    average_runtimes = np.zeros((len(num_enemies_list), len(maze_sizes)))
    average_moves = np.zeros((len(num_enemies_list), len(maze_sizes)))

    for i, num_enemies in enumerate(num_enemies_list):
        for j, maze_size in enumerate(maze_sizes):
            runtimes, moves = run_simulations(num_runs, agent_type, num_agents, num_enemies, maze_size)
            average_runtimes[i, j] = calculate_average(runtimes)
            average_moves[i, j] = calculate_average(moves)  # Add this line to get the average moves
    
    return average_runtimes, average_moves

# Plot a heatmap of average moves for a specific agent type based on the number of enemies and maze size
def plot_agent_type_moves(agent_type, num_agents, average_moves, num_enemies_list, maze_sizes, ax):
    
    im = ax.imshow(average_moves)

    ax.set_xticks(np.arange(len(maze_sizes)))
    ax.set_yticks(np.arange(len(num_enemies_list)))
    ax.set_xticklabels(maze_sizes)
    ax.set_yticklabels(num_enemies_list)

    ax.set_xlabel("Maze Size")
    ax.set_ylabel("Number of Enemies")
    ax.set_title(f"Average Moves for Agent Type {agent_type}, Number of Agents: {num_agents}")

    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Average Moves", rotation=-90, va="bottom")

    # Show the average moves in each cell
    for i in range(len(num_enemies_list)):
        for j in range(len(maze_sizes)):
            text = ax.text(j, i, f"{average_moves[i, j]:.2f} moves", ha="center", va="center", color="w")


def plot_agent_type_runtimes(agent_type, num_agents, average_runtimes, num_enemies_list, maze_sizes, ax):
    
    im = ax.imshow(average_runtimes)

    ax.set_xticks(np.arange(len(maze_sizes)))
    ax.set_yticks(np.arange(len(num_enemies_list)))
    ax.set_xticklabels(maze_sizes)
    ax.set_yticklabels(num_enemies_list)

    ax.set_xlabel("Maze Size")
    ax.set_ylabel("Number of Enemies")
    ax.set_title(f"Average Runtime for Agent Type {agent_type}")

    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Average Runtime (seconds)", rotation=-90, va="bottom")

    # Show the average runtimes in each cell
    for i in range(len(num_enemies_list)):
        for j in range(len(maze_sizes)):
            text = ax.text(j, i, f"{average_runtimes[i, j]:.2f} sec", ha="center", va="center", color="w")



# Main part of the code
selected_agent_type = A_STAR_AGENT
DYNAMIC_ENEMIES = True
selected_num_agents = 1

# Parameter ranges
agent_types = [RULE_BASED_AGENT, A_STAR_AGENT, Q_TABLE_AGENT]
num_agents_list = [1, 2, 3]
num_enemies_list = [1, 3]
maze_sizes = [40, 20]

num_runs = 5

# Run the simulations and plot the results
average_runtimes, average_moves = run_agent_type_simulations(selected_agent_type, selected_num_agents, num_enemies_list, maze_sizes, num_runs)

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot the heatmap of average runtimes
plot_agent_type_runtimes(selected_agent_type, selected_num_agents, average_runtimes, num_enemies_list, maze_sizes, ax1)

# Plot the heatmap of average moves
plot_agent_type_moves(selected_agent_type, selected_num_agents, average_moves, num_enemies_list, maze_sizes, ax2)

# Show the combined plot
plt.show()


