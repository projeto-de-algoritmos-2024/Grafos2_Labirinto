import pygame
import random
import sys
from ttkthemes import ThemedTk
from tkinter import ttk


class Labirinto:
    def __init__(self, width, height, tile_size):
        self.tile_size = tile_size
        self.rows = height // tile_size
        self.cols = width // tile_size
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Grafos 2 Labirinto")

    def draw_maze(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
        pygame.display.flip()

    def is_within_bounds(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def generate_maze(self, start_x, start_y):
        stack = [(start_x, start_y)]
        self.grid[start_y][start_x] = 1

        while stack:
            x, y = stack[-1]
            directions = self.directions[:]
            random.shuffle(directions)

            found_path = False
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if self.is_within_bounds(nx, ny) and self.grid[ny][nx] == 0:
                    self.grid[y + dy][x + dx] = 1
                    self.grid[ny][nx] = 1
                    stack.append((nx, ny))
                    found_path = True
                    break

            if not found_path:
                stack.pop()

            if len(stack) % 500 == 0:
                self.draw_maze()

    def draw_path(self, x, y):
        pygame.draw.rect(self.screen, (0, 0, 255), (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
        pygame.display.flip()

    def DFS(self, start, end):
        stack = [start]
        visited = set()
        clock = pygame.time.Clock()

        while stack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))

            self.draw_path(x, y)

            if (x, y) == end:
                print("Ponto de destino encontrado!")
                break

            if self.grid[y][x] == 1:
                for dx, dy in self.directions:
                    nx, ny = x + dx, y + dy
                    if self.is_within_bounds(nx, ny) and self.grid[ny][nx] == 1 and (nx, ny) not in visited:
                        stack.append((nx, ny))

            clock.tick(10000)

def main(algoritmo):
    pygame.init()
    infoObject = pygame.display.Info()
    width, height = infoObject.current_w, infoObject.current_h
    tile_size = 5

    labirinto = Labirinto(width, height, tile_size)
    labirinto.generate_maze(0, 0)
    labirinto.draw_maze()
    if algoritmo == "Djstra":
        print("aaaaa")
    elif algoritmo == "DFS":
        labirinto.DFS((0, 0), (width-2, height-2))
    elif algoritmo == "BogoSort":
        print("bbbb")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
    sys.exit()

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def salvar_input():
    algoritmo = combobox.get()
    print(f"Algoritmo selecionado: {algoritmo}")
    janela.destroy()
    main(algoritmo)


if __name__ == "__main__":

    janela = ThemedTk(theme="adapta")
    janela.title("Grafo2-Labirinto")
    janela.configure(bg="white")

    largura = 400
    altura = 200
    centralizar_janela(janela, largura, altura)

    label = ttk.Label(janela, text="Labirinto", font=("Arial", 24))
    label.pack(pady=20)

    combobox = ttk.Combobox(janela, values=["Djstra", "DFS", "BogoSort"], font=("Arial", 10), justify='center')
    combobox.pack(pady=10)
    combobox.set("Djstra")

    botao = ttk.Button(janela, text="Gerar Labirinto", command=salvar_input)
    botao.pack(pady=10)

    janela.mainloop()

