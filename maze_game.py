import pygame
import random
from collections import deque

CELL_SIZE = 13  # 每個格子13x13像素


# 迷宮方格類別
class Tile:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # "path" 或 "wall"

    def draw(self, screen, font):
        color = (255, 255, 255) if self.type == "path" else (0, 0, 0)
        pygame.draw.rect(
            screen,
            color,
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            1,
        )

        # 開始與結束標記
        if (self.x, self.y) == (1, 1):
            text = font.render("開始", True, (255, 0, 0))
            screen.blit(text, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        elif (self.x, self.y) == (40, 40):
            text = font.render("結束", True, (0, 200, 0))
            screen.blit(text, (self.x * CELL_SIZE, self.y * CELL_SIZE))


# 迷宮類別
class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Tile(x, y, "wall") for y in range(height)] for x in range(width)]
        self.generate_maze()

    def generate_maze(self):
        # 先用 DFS 生成迷宮，確保有一條可以走的路
        path = self.generate_maze_dfs((1, 1), (40, 40))
        for x, y in path:
            self.grid[x][y].type = "path"

        # 加入更多隨機牆壁，提高迷宮難度 (牆壁機率提高)
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if (
                    x,
                    y,
                ) not in path and random.random() < 0.65:  # 增加牆壁機率 (原來是 55%)
                    self.grid[x][y].type = "wall"
                else:
                    self.grid[x][y].type = "path"

        # 邊界為牆
        for x in range(self.width):
            self.grid[x][0].type = "wall"
            self.grid[x][self.height - 1].type = "wall"
        for y in range(self.height):
            self.grid[0][y].type = "wall"
            self.grid[self.width - 1][y].type = "wall"

    def generate_maze_dfs(self, start, end):
        visited = set()
        stack = [start]
        path = []

        while stack:
            x, y = stack[-1]
            if (x, y) == end:
                path.append((x, y))
                break

            visited.add((x, y))
            neighbors = [
                (x + dx, y + dy) for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]
            ]
            random.shuffle(neighbors)

            for nx, ny in neighbors:
                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and (nx, ny) not in visited
                ):
                    stack.append((nx, ny))
                    path.append((nx, ny))
                    break
            else:
                stack.pop()

        return path

    def draw(self, screen, font):
        for row in self.grid:
            for tile in row:
                tile.draw(screen, font)

    def is_move_valid(self, x, y):
        return (
            0 <= x < self.width
            and 0 <= y < self.height
            and self.grid[x][y].type == "path"
        )


# 玩家類別
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 128, 255)

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if maze.is_move_valid(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )


# 遊戲類別
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((CELL_SIZE * 42, CELL_SIZE * 42))
        pygame.display.set_caption("迷宮遊戲")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 11)
        self.maze = Maze(42, 42)
        self.player = Player(1, 1)
        self.running = True

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.move(-1, 0, self.maze)
            elif event.key == pygame.K_RIGHT:
                self.player.move(1, 0, self.maze)
            elif event.key == pygame.K_UP:
                self.player.move(0, -1, self.maze)
            elif event.key == pygame.K_DOWN:
                self.player.move(0, 1, self.maze)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_input(event)

            self.screen.fill((0, 0, 0))
            self.maze.draw(self.screen, self.font)
            self.player.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()


# 主函數
def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
