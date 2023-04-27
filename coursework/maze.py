import random
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Maze:
    def __init__(self, screen_width, screen_height, cell_size):
        self.cell_size = cell_size
        self.width = screen_width // cell_size
        self.height = screen_height // cell_size
        self.maze = []
        self.create_maze()

    def create_maze(self):
        raise NotImplementedError

    def draw(self, screen):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(screen, BLACK, [j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size])
                else:
                    pygame.draw.rect(screen, WHITE, [j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size])

    def print_maze(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 1:
                    print("#", end="")
                else:
                    print(" ", end="")
            print()
            
    def get_neighbors(self, cell):
        i, j = cell
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        neighbors = [x for x in neighbors if x[1] > 0 and x[1] < self.height and x[0] > 0 and x[0] < self.width]
        neighbors = [x for x in neighbors if self.maze[x[1]][x[0]] == 0]
        return neighbors


            
class RandomMaze(Maze):
    
    def create_maze(self):
    
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1:
                    row.append(1)
                else:
                    row.append(0)
            self.maze.append(row)

        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if random.randint(0, 100) < 20:
                    self.maze[i][j] = 1
    

class FixedMaze(Maze):
    def __init__(self, screen_width, screen_height, cell_size):
        super().__init__(screen_width, screen_height, cell_size)
        self.cell_size = 80
        self.width = 10
        self.height = 10
        
    def create_maze(self):
        self.maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]



class PrimMaze(Maze):
    def create_maze(self):
        # Initialize the maze with all walls
        self.maze = [[1] * self.width for i in range(self.height)]
        
        # Choose a random starting point
        x = random.randrange(1, self.width - 1, 2)
        y = random.randrange(1, self.height - 1, 2)
        self.maze[y][x] = 0
        
        # Initialize the frontier
        frontier = [(x, y)]
        
        # Create the maze using the Prim's algorithm
        while frontier:
            x, y = random.choice(frontier)
            frontier.remove((x, y))
            
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if nx < 1 or nx >= self.width - 1 or ny < 1 or ny >= self.height - 1:
                    continue
                if self.maze[ny][nx] == 1:
                    self.maze[ny][nx] = 0
                    self.maze[y + dy//2][x + dx//2] = 0
                    frontier.append((nx, ny))

