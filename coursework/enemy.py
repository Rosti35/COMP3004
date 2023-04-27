import pygame
import random

RED = (255, 0, 0)

class Enemy:
    def __init__(self, x, y, size, maze):
        self.rect = pygame.Rect(x, y, size, size)
        self.maze = maze
        self.speed = size
    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
        
    def set_random_position(self):
        while True:
            x = random.randint(0, len(self.maze.maze[0]) - 1)
            y = random.randint(0, len(self.maze.maze) - 1)
            if self.maze.maze[y][x] != 1:
                self.rect.x = x * self.maze.cell_size
                self.rect.y = y * self.maze.cell_size
                break

    def update(self):
        
        wall_rects = [pygame.Rect(j * self.maze.cell_size, i * self.maze.cell_size, self.maze.cell_size, self.maze.cell_size) for i in range(len(self.maze.maze)) for j in range(len(self.maze.maze[0])) if self.maze.maze[i][j] == 1]
        
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
