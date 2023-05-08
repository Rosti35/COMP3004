import pygame
import random
import math
import time
import heapq
import numpy as np
import pprint

GREEN = (0, 255, 0)
GRAY = (128,128,128)



class Agent:
    def __init__(self, x, y, size, maze):
        self.rect = pygame.Rect(x, y, size, size)
        self.maze = maze
        self.dx = x
        self.dy = y
        self.speed = size
        self.path = []

    def update(self, dx, dy, enemies):
        raise NotImplementedError

                        
    def set_random_position(self):
        while True:
            x = random.randint(0, len(self.maze.maze[0]) - 1)
            y = random.randint(0, len(self.maze.maze) - 1)
            if self.maze.maze[y][x] != 1:
                self.rect.x = x * self.maze.cell_size
                self.rect.y = y * self.maze.cell_size
                break

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)
        
    def find_nearest_enemy(self, enemies):
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = math.sqrt((self.rect.centerx - enemy.rect.centerx) ** 2 + (self.rect.centery - enemy.rect.centery) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        return nearest_enemy
    
    def draw_path(self, screen):
        if self.path is not None:
            for p in self.path:
                pygame.draw.rect(screen, GRAY, pygame.Rect(p[0]*self.speed, p[1]*self.speed, self.speed, self.speed))

class RuleBasedAgent(Agent):
    def update(self, enemies):
        
        # Find the nearest enemy
        nearest_enemy = self.find_nearest_enemy(enemies)

        # Move towards the nearest enemy
        if nearest_enemy is not None:
            dx = nearest_enemy.rect.centerx - self.rect.centerx
            dy = nearest_enemy.rect.centery - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            print(f"Distance: {distance}")
            if distance != 0:
                if abs(dx) > abs(dy):
                    self.dx = round(dx / abs(dx))
                    self.dy = 0
                else:
                    self.dx = 0
                    self.dy = round(dy / abs(dy))
                print(f"dx: {self.dx}, dy: {self.dy}")
                print(f"Moving towards enemy at ({nearest_enemy.rect.centerx}, {nearest_enemy.rect.centery})")
                
            next_pos = self.rect.move(self.dx * self.speed, self.dy * self.speed)

            # Check for collisions with walls
            wall_rects = [pygame.Rect(j * self.maze.cell_size, i * self.maze.cell_size, self.maze.cell_size, self.maze.cell_size) for i in range(len(self.maze.maze)) for j in range(len(self.maze.maze[0])) if self.maze.maze[i][j] == 1]
            wall_collisions = [next_pos.colliderect(wall_rect) for wall_rect in wall_rects]
            if True in wall_collisions:
                # Choose a random direction that does not have a wall
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                while True:
                    random_direction = random.choice(directions)
                    new_rect = self.rect.move(random_direction[0] * self.maze.cell_size, random_direction[1] * self.maze.cell_size)
                    wall_collisions = [new_rect.colliderect(wall_rect) for wall_rect in wall_rects]
                    if True not in wall_collisions:
                        self.dx, self.dy = random_direction
                        break
                    
            # Move the agent
            self.rect.x += self.dx * self.speed
            self.rect.y += self.dy * self.speed
            print(f"Moved to ({self.rect.centerx}, {self.rect.centery})")   

# Define heuristic function
def heuristic(a, b):
    # Calculate the Euclidean distance
    dx = abs(a[1] - b[1])
    dy = abs(a[0] - b[0])
    h = math.sqrt(dx * dx + dy * dy)
    
    return h

class AStarAgent(Agent):
    
    def update(self,enemies):
        
        
        # Find the nearest enemy
        nearest_enemy = self.find_nearest_enemy(enemies)
        
        # Find a new path if needed
        if nearest_enemy is not None and self.path is not None:
        
            start = (self.rect.x // self.speed, self.rect.y // self.speed)
            end = (nearest_enemy.rect.x // self.speed, nearest_enemy.rect.y // self.speed)
            self.path = self.find_path(start, end)
            if self.path is not None:
                self.path.pop(0)
            print(self.path)
            
            
        if self.path is not None and len(self.path)>0:
            x, y = self.path.pop(0)
            self.rect.x = x * self.speed
            self.rect.y = y * self.speed

    def find_path(self, start, end):
        # Initialize the A* algorithm
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, end)}

        # Run the A* algorithm
        while len(open_set) > 0:
            current = heapq.heappop(open_set)[1]
            print(f"current: {current}")
            if current == end:
                path = [end]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            neighbors = self.maze.get_neighbors(current)
            print(list(neighbors))
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                    if neighbor not in [x[1] for x in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        
                        
class QLearningAgent(Agent):
    def __init__(self, x, y, size, maze, alpha=0.1, gamma=0.99, epsilon=0.1, episodes=100):
        super().__init__(x, y, size, maze)
        self.q_table = np.zeros((maze.height, maze.width, 4))  # 4 actions: up, down, left, right
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.episodes = episodes

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(4)  # Random action (exploration)
        else:
            return np.argmax(self.q_table[state[0], state[1]])  # Best action 

    def update(self, enemies):
       
            nearest_enemy = self.find_nearest_enemy(enemies)

            if nearest_enemy is not None:
                for _ in range(self.episodes):
                    start = (self.rect.y // self.speed, self.rect.x // self.speed)
                    end = (nearest_enemy.rect.y // self.speed, nearest_enemy.rect.x // self.speed)
                    state = start
                    while not self.is_goal(state, nearest_enemy):
                        action = self.choose_action(state)
                        next_state = self.get_next_state(state, action)
                        reward = self.calculate_reward(state, next_state, end)
                        self.update_q_table(state, action, next_state, reward)
                        state = next_state

                # Move agent based on the learned Q-values
                state = (self.rect.y // self.speed, self.rect.x // self.speed)
                if not self.is_goal(state, nearest_enemy):
                    action = np.argmax(self.q_table[state[0], state[1]]) # Best action 
                    next_state = self.get_next_state(state, action)
                    self.rect.y, self.rect.x = next_state[0] * self.speed, next_state[1] * self.speed

    def get_next_state(self, state, action):
        next_state = list(state)
        if action == 0:  # Up
            next_state[0] = max(0, state[0] - 1)
        elif action == 1:  # Down
            next_state[0] = min(self.maze.height - 1, state[0] + 1)
        elif action == 2:  # Left
            next_state[1] = max(0, state[1] - 1)
        elif action == 3:  # Right
            next_state[1] = min(self.maze.width - 1, state[1] + 1)
        return tuple(next_state)

    def calculate_reward(self, state, next_state, end):
        if self.maze.maze[next_state[0]][next_state[1]] == 1:
            return -1000  # Penalty for hitting a wall
        if next_state == end:
            return 100  # Reward for reaching the goal
        return -1  # Small penalty for each step

    def update_q_table(self, state, action, next_state, reward):
        q_next_max = np.max(self.q_table[next_state[0], next_state[1]])
        self.q_table[state[0], state[1], action] += self.alpha * (reward + self.gamma * q_next_max - self.q_table[state[0], state[1], action])

    def is_goal(self, state, nearest_enemy):
        goal_state = (nearest_enemy.rect.y // self.speed, nearest_enemy.rect.x // self.speed)
        return state == goal_state



