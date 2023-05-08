        # Check for collisions with walls
        # for i in range(len(self.maze.maze)):
        #     for j in range(len(self.maze.maze[0])):
        #         if self.maze.maze[i][j] == 1:
        #             wall_rect = pygame.Rect(j * self.maze.cell_size, i * self.maze.cell_size, self.maze.cell_size, self.maze.cell_size)
        #             if self.rect.colliderect(wall_rect):
        #                 # Try moving in the opposite direction
        #                 if self.dx > 0:
        #                     print(1)
        #                     self.rect.right = wall_rect.left
        #                     # self.dx = 0
        #                     # self.dy = 1
        #                 elif self.dx < 0:
        #                     print(2)
        #                     self.rect.left = wall_rect.right
        #                     # self.dx = 0
        #                     # self.dy = -1
        #                 elif self.dy > 0:
        #                     print(3)
        #                     self.rect.bottom = wall_rect.top
        #                     # self.dy = 0
        #                     # self.dx = 1
        #                 elif self.dy < 0:
        #                     print(4)
        #                     self.rect.top = wall_rect.bottom
        #                     # self.dy = 0
        #                     # self.dx = -1
        #                 print(f"Hit wall at ({self.rect.centerx}, {self.rect.centery}), changing direction to ({self.dx}, {self.dy})")
        #                 time.sleep(0.5)