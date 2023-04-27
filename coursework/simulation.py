import pygame
from maze import *
from agent import *
from enemy import *
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Simulation:
    def __init__(self, screen_width, screen_height):
        pygame.init()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.size = None
        self.maze = None
        self.agents = []
        self.running = False
        self.enemies = []
        self.moves = 0

    def new_simulation(self):
        raise NotImplementedError
    
    def stop_simulation(self):
        self.running = False
        
    def get_moves(self):
        return self.moves
 
    def run(self):
        
        self.running = True
        enemy_update_interval = 300  # Update enemies every 300 milliseconds (0.3 seconds)
        last_enemy_update = pygame.time.get_ticks()  # Keep track of the last time enemies were updated

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the cell position from the mouse click
                    cell_x, cell_y = event.pos[0] // self.size, event.pos[1] // self.size

                    # Check if the cell is free
                    if self.maze.maze[cell_y][cell_x] != 1:
                        # Create a new enemy at the clicked position
                        new_enemy = Enemy(cell_x * self.size, cell_y * self.size, self.size, self.maze);
                        self.enemies.append(new_enemy)

            # Update agents
            for agent in self.agents:
                agent.update(self.enemies)

            self.moves += 1
            
            # Check if it's time to update the enemies
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_update >= enemy_update_interval:
                # for enemy in self.enemies:
                #     enemy.update()
                last_enemy_update = current_time  # Update the last_enemy_update time

            # Check for collisions between agents and enemies
            for agent in self.agents:
                for enemy in self.enemies:
                    if agent.rect.colliderect(enemy.rect):
                        self.enemies.remove(enemy)

            # Clear the screen
            self.screen.fill(WHITE)

            # Draw the maze, player, and enemies
            self.maze.draw(self.screen)
            
            for agent in self.agents:
                agent.draw_path(self.screen)
                agent.draw(self.screen)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Update the screen
            pygame.display.flip()

            # Set the frame rate
            self.clock.tick(60)
            
            if len(self.enemies) == 0:
                break

        # Quit the game
        pygame.quit()
        
    def quit(self):
        pygame.quit()
 

class FixedMazeSimulation(Simulation):
    def new_simulation(self, agent_type):
        self.size = 80
        # Create the maze
        self.maze = FixedMaze(self.screen_width, self.screen_width, self.size)
        # self.maze.print_maze()

        # Spawn agents
        if agent_type == 0:
            agent = RuleBasedAgent(8 * self.size , 1 * self.size, self.size, self.maze)
        elif agent_type == 1:
            agent = AStarAgent(8 * self.size , 1 * self.size, self.size, self.maze)
        else:
            agent = QLearningAgent(8 * self.size , 1 * self.size, self.size, self.maze)

        self.agents.append(agent)
        
        # Spawn some enemies
        e = Enemy(5 * self.size , 3 * self.size, self.size, self.maze);
        self.enemies.append(e)
        e = Enemy(1 * self.size , 8 * self.size, self.size, self.maze);
        self.enemies.append(e)


class RandomMazeSimulation(Simulation):
    def new_simulation(self, agent_type, num_agents, num_enemies, size):
        self.size = size
        # Create the maze
        self.maze = RandomMaze(self.screen_width, self.screen_width, size)
        # self.maze.print_maze()

        # Spawn agents
        self.agents = spawn_agents(num_agents, size, self.maze, agent_type)

        # Spawn some enemies
        self.enemies = spawn_enemies(num_enemies, size, self.maze)
        
class PrimMazeSimulation(Simulation):
    def new_simulation(self, agent_type, num_agents, num_enemies, size):
        self.size = size
        # Create the maze
        self.maze = PrimMaze(self.screen_width, self.screen_width, size)
        # self.maze.print_maze()

        # Spawn agents
        self.agents = spawn_agents(num_agents, size, self.maze, agent_type)

        # Spawn some enemies
        self.enemies = spawn_enemies(num_enemies, size, self.maze)
      
def spawn_enemies(num_enemies, size, maze):
    enemies = []
    for _ in range(num_enemies):
        # Create an enemy with a random position
        e = Enemy(0, 0, size, maze)
        e.set_random_position()
        print(f"Enemy pos: ({e.rect.x}, {e.rect.y})")
        enemies.append(e)
    return enemies

def spawn_agents(num_agents, size, maze, agent_type):
    agents = []
    for _ in range(num_agents):
        if agent_type == 0:
            agent = RuleBasedAgent(0, 0, size, maze)
        elif agent_type == 1:
            agent = AStarAgent(0, 0, size, maze)
        else:
            agent = QLearningAgent(0, 0, size, maze)
        agent.set_random_position()
        agents.append(agent)
    return agents

# def print_env(maze, agent, enemys, size):
#     for i in range(len(maze)):
#         for j in range(len(maze[0])):
#             if maze[i][j] == 1:
#                 print("#", end="")
#             else:
#                 if agent.rect.x // size == i and 
#                 print(" ", end="")
#         print()