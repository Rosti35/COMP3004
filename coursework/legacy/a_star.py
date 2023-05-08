import pygame
import random
import heapq
import time

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Define cell size
CELL_SIZE = 10

# Define heuristic function
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
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
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(screen, BLACK, [j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE])
                else:
                    pygame.draw.rect(screen, WHITE, [j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE])

    def get_neighbors(self, cell):
        i, j = cell
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        neighbors = filter(lambda x: x[0] >= 0 and x[0] < self.height and x[1] >= 0 and x[1] < self.width, neighbors)
        neighbors = filter(lambda x: self.maze[x[0]][x[1]] != 1, neighbors)
        return neighbors

class Player:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.maze = maze
        self.path = []

    def update(self):
        if len(self.path) > 0:
            x, y = self.path.pop(0)
            self.rect.x = x * CELL_SIZE
            self.rect.y = y * CELL_SIZE

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

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
            if current == end:
                path = [end]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            for neighbor in self.maze.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                    if neighbor not in [x[1] for x in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    def move_to(self, x, y):
        start = (self.rect.x // CELL_SIZE, self.rect.y // CELL_SIZE)
        end = (x, y)
        self.path = self.find_path(start, end)

    # def set_random_position(self):
    #         while True:
    #             x = random.randint(0, len(self.maze.maze[0]) - 1)
    #             y = random.randint(0, len(self.maze.maze) - 1)
    #             if self.maze.maze[y][x] != 1:
    #                 self.rect.x = x * self.maze.cell_size
    #                 self.rect.y = y * self.maze.cell_size
    #                 break
                
    def handle_input(self):
        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_to((self.rect.x - CELL_SIZE) // CELL_SIZE, self.rect.y // CELL_SIZE)
        elif keys[pygame.K_RIGHT]:
            self.move_to((self.rect.x + CELL_SIZE) // CELL_SIZE, self.rect.y // CELL_SIZE)
        elif keys[pygame.K_UP]:
            self.move_to(self.rect.x // CELL_SIZE, (self.rect.y - CELL_SIZE) // CELL_SIZE)
        elif keys[pygame.K_DOWN]:
            self.move_to(self.rect.x // CELL_SIZE, (self.rect.y + CELL_SIZE) // CELL_SIZE)
    


if __name__ == "__main__":
    # Initialize the game
    pygame.init()

    # Set the screen size
    screen_width = 1000
    screen_height = 1000
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Create the maze and player
    maze = Maze(50, 50)
    player = Player(1, 1, maze)
    # player.set_random_position()

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Find a new path if needed
        if len(player.path) == 0:
            start = (player.rect.y // CELL_SIZE, player.rect.x // CELL_SIZE)
            end = (random.randint(0, maze.height - 1), random.randint(0, maze.width - 1))
            player.path = player.find_path(start, end)

        # Update the player
        player.update()
        time.sleep(0.5)

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


