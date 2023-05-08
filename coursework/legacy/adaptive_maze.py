import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)

class Maze:
    def __init__(self, screen_width, screen_height, cell_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.width = int(screen_width / cell_size)
        self.height = int(screen_height / cell_size)
        self.maze = self.create_maze()

    def create_maze(self):
        maze = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1:
                    row.append(1)
                else:
                    row.append(0)
            maze.append(row)

        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if random.randint(0, 100) < 20:
                    maze[i][j] = 1

        return maze

    def draw(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(screen, BLACK, [j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size])

class Player:
    def __init__(self, x, y, width, height, maze, cell_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.maze = maze
        self.cell_size = cell_size

    def update(self, dx, dy):
        # Move the player
        self.rect.x += dx
        self.rect.y += dy

        # Check for collisions with walls
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.maze.maze[i][j] == 1:
                    wall_rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                    if self.rect.colliderect(wall_rect):
                        if dx > 0:
                            self.rect.right = wall_rect.left
                        elif dx < 0:
                            self.rect.left = wall_rect.right
                        elif dy > 0:
                            self.rect.bottom = wall_rect.top
                        elif dy < 0:
                            self.rect.top = wall_rect.bottom

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

if __name__ == "__main__":
    # Initialize the game
    pygame.init()

    # Set the screen size and cell size
    screen_width = 800
    screen_height = 800
    cell_size = 10
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Create the maze and player
    maze = Maze(screen_width, screen_height, cell_size)
    player = Player(cell_size, cell_size, cell_size, cell_size, maze, cell_size)

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the player
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5
        player.update(dx, dy)

        # Clear the screen
        screen.fill(WHITE)

        # Draw the maze and player
        maze.draw(screen)
        player.draw(screen)

        # Update the screen
        pygame.display.flip()

        # Set the frame rate
        clock = pygame.time.Clock()
        clock.tick(60)

    # Quit the game
    pygame.quit()

