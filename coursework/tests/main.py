import pygame

from maze import *
from agent import Player

WHITE = (255, 255, 255)

if __name__ == "__main__":
    # Initialize the game
    pygame.init()

    # Set the screen size
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Create the maze and player
    maze = FixedMaze(screen_width, screen_width, 80)
    player = Player(0, 0, 20, 20, maze)
    player.set_random_position()
    # Print the maze
    maze.print_maze()

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
        #print("Clear the screen!")
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

