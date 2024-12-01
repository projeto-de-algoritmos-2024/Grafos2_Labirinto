import pygame
import random
import sys
from ttkthemes import ThemedTk
from tkinter import ttk
import heapq
import math


class Labirinto:
    def __init__(self, width, height, tile_size):
        self.tile_size = tile_size
        self.rows = height // tile_size
        self.cols = width // tile_size
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.weights = [[1] * self.cols for _ in range(self.rows)]  
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Grafos 2 Labirinto")
        self.red_points = []

    def draw_maze(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == 1:
                    color = (255, 0, 0) if self.weights[y][x] == 2 else (255, 255, 255)
                    pygame.draw.rect(self.screen, color, (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                
        for rx, ry in self.red_points:
            pygame.draw.rect(self.screen, (255, 0, 0), (rx * self.tile_size, ry * self.tile_size, self.tile_size, self.tile_size))
        

        pygame.display.flip()

    def is_within_bounds(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def generate_maze_normal(self, start_x, start_y):
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

            if len(stack) % 200 == 0:
                self.draw_maze()

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
                    if random.random() < 0.3: 
                        self.weights[y + dy][x + dx] = 2
                    stack.append((nx, ny))
                    found_path = True
                    break

            if not found_path:
                stack.pop()

            if len(stack) % 200 == 0:
                self.draw_maze()
    
    def draw_path(self, x, y):
        pygame.draw.rect(self.screen, (0, 0, 255), (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
        pygame.display.flip()

    def draw_cell(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
        pygame.time.wait(10)
        pygame.display.update()

    def dijkstra(self, start, end):
        queue = [(0, start)]
        distances = {start: 0}
        previous = {start: None}
        visited = set()

        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            current_distance, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)

            x, y = current
            self.draw_cell(x, y, (0, 255, 0))

            print(current)
            if current == end:
                path = []
                while current:
                    path.append(current)
                    current = previous[current]
                path.reverse()

                for px, py in path:
                    self.draw_cell(px, py, (0, 0, 255))  
                return
            
            cx, cy = current
            for dx, dy in self.directions:
                nx, ny = cx + dx, cy + dy
                if self.is_within_bounds(nx, ny) and self.grid[ny][nx] == 1:
                    neighbor = (nx, ny)
                    new_distance = current_distance + self.weights[ny][nx]

                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
                        heapq.heappush(queue, (new_distance, neighbor))

    def generate_red_points(self, num_points):
        valid_points = []
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == 1:
                    valid_points.append((x, y))
        
        self.red_points = random.sample(valid_points, min(num_points, len(valid_points)))

    def euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def dijkstra_prim(self, start, end):
        queue = [(0, start)]
        distances = {start: 0}
        previous = {start: None}
        visited = set()

        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            current_distance, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)

            if current == end:
                path = []
                while current:
                    path.append(current)
                    current = previous[current]
                return list(reversed(path))
            
            cx, cy = current
            for dx, dy in self.directions:
                nx, ny = cx + dx, cy + dy
                if self.is_within_bounds(nx, ny) and self.grid[ny][nx] == 1:
                    neighbor = (nx, ny)
                    new_distance = current_distance + 1

                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
                        heapq.heappush(queue, (new_distance, neighbor))

        return []

    def prim_algorithm(self, start):
        unvisited_points = self.red_points.copy()
        current_point = start
        total_path = []
        visited_points = [current_point]
        unvisited_points.remove(current_point)

        while unvisited_points:
            nearest_point = min(unvisited_points, key=lambda p: self.euclidean_distance(current_point, p))
            path = self.dijkstra_prim(current_point, nearest_point)
            total_path.extend(path[:-1])  
            current_point = nearest_point
            visited_points.append(current_point)
            unvisited_points.remove(current_point)

        return total_path

    def visualize_path(self, path):
        for px, py in path:
            self.draw_cell(px, py, (0, 0, 255)) 
            pygame.time.wait(10)

    def draw_cell(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
        pygame.display.update()

def main(algoritmo, width, height, num_red_points):
    pygame.init()
    tile_size = 5

    labirinto = Labirinto(width, height, tile_size)

    if algoritmo == "Prim":
        labirinto.generate_maze_normal(0, 0)
        labirinto.generate_red_points(num_red_points)
        labirinto.draw_maze()
        start = labirinto.red_points[0]
        path = labirinto.prim_algorithm(start)
        labirinto.visualize_path(path)
    elif algoritmo == "Dijkstra":
        labirinto.generate_maze(0, 0)
        labirinto.draw_maze()
        start = (0, 0)
        end = (labirinto.cols - 2, labirinto.rows - 2)
        labirinto.dijkstra(start, end)

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
    largura_labirinto = largura_entry.get()
    if int(largura_labirinto) > 600:
        largura_labirinto = 600
    altura_labirinto = altura_entry.get()
    if int(altura_labirinto) > 600:
        altura_labirinto = 600
    num_pontos_vermelhos = pontos_vermelhos_entry.get()
    
    print(f"Largura: {largura_labirinto}, Altura: {altura_labirinto}, Pontos Vermelhos: {num_pontos_vermelhos}")
    janela.destroy()
    main(algoritmo, int(largura_labirinto), int(altura_labirinto), int(num_pontos_vermelhos))

if __name__ == "__main__":
    janela = ThemedTk(theme="adapta")
    janela.title("Grafo2-Labirinto")
    janela.configure(bg="white")

    largura = 400
    altura = 400
    centralizar_janela(janela, largura, altura)

    label = ttk.Label(janela, text="Labirinto", font=("Arial", 24))
    label.pack(pady=20)

    label_largura = ttk.Label(janela, text="Largura do labirinto:", font=("Arial", 10))
    label_largura.pack(pady=5)
    largura_entry = ttk.Entry(janela, font=("Arial", 10))
    largura_entry.insert(0, "500")
    largura_entry.pack(pady=5)

    label_altura = ttk.Label(janela, text="Altura do labirinto:", font=("Arial", 10))
    label_altura.pack(pady=5)
    altura_entry = ttk.Entry(janela, font=("Arial", 10))
    altura_entry.insert(0, "500")
    altura_entry.pack(pady=5)

    label_pontos_vermelhos = ttk.Label(janela, text="Número de pontos vermelhos:", font=("Arial", 10))
    pontos_vermelhos_entry = ttk.Entry(janela, font=("Arial", 10))
    

    def atualizar_visibilidade(event):
        if combobox.get() == "Prim":
            label_pontos_vermelhos.pack(pady=5)
            pontos_vermelhos_entry.insert(0, "0")
            pontos_vermelhos_entry.pack(pady=5)
        else:
            label_pontos_vermelhos.pack_forget()
            pontos_vermelhos_entry.pack_forget()

    combobox = ttk.Combobox(janela, values=["Dijkstra", "Prim"], font=("Arial", 10), justify='center')
    combobox.pack(pady=10)
    combobox.set("Prim")
    combobox.bind("<<ComboboxSelected>>", atualizar_visibilidade)

    atualizar_visibilidade(None)

    botao = ttk.Button(janela, text="Gerar Labirinto", command=salvar_input)
    botao.pack(pady=10)

    janela.mainloop()
