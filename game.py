import pygame
import sys
import random

# Impostazioni generali
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30

# WIDTH // GRID_SIZE calcola quante colonne entrano nella larghezza dell'area
# HEIGHT // GRID_SIZE: calcola quante righe entrano nell'altezza dell'area
COLUMNS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
NEXT_PIECES_POS = (WIDTH + 50, 50)

# Colori
BLACK, WHITE, GRAY = (0, 0, 0), (255, 255, 255), (128, 128, 128)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
          (255, 165, 0), (128, 0, 128), (0, 255, 255)]

# Forme Tetris
SHAPES = [
    #I
    [[1, 1, 1, 1]],
    #0
    [[1, 1], [1, 1]],
    #S
    [[1, 1, 0], [0, 1, 1]],
    #Z
    [[0, 1, 1], [1, 1, 0]],
    #E
    [[1, 1, 1], [0, 1, 0]],
    #L
    [[1, 1, 1], [1, 0, 0]],
    #J
    [[1, 1, 1], [0, 0, 1]]
]

LEVEL_LINE_GOAL = 10 
MAX_LEVEL = 15

class Piece:
    def __init__(self, shape=None):
        self.shape = shape or random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        #COLUMNS//2 trova la colonna centrale del campo, len(self.shape[0]) // 2 trova la metà della larghezza del pezzo.
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        #per ruotare una matrice 2D (un pezzo del gioco) di 90° in senso orario, 
        #aggiornando self.shape trasformandola in una nuova lista di liste, che rappresenta la figura ruotata.


def check_collision(grid, piece, offset_x=0, offset_y=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                nx = piece.x + x + offset_x
                ny = piece.y + y + offset_y
                #x,y sono la posizione della cella e piece.x/y del pezzo
                if nx < 0 or nx >= COLUMNS or ny >= ROWS or (ny >= 0 and grid[ny][nx]):
                    #nx < 0 or nx >= COLUMNS se la cella va fuori dai bordi orizzontali
                    #ny >= ROWS se la cella scende oltre il fondo
                    #ny >= 0 and grid[ny][nx] se anche una sola cella del pezzo collide (con bordi o altre celle)
                    return True
    return False


def merge_piece(grid, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell and piece.y + y >= 0:
                grid[piece.y + y][piece.x + x] = piece.color


def clear_lines(grid):
    cleared = 0
    full_rows = [i for i, row in enumerate(grid) if all(row)]
    for i in full_rows:
        del grid[i]
        grid.insert(0, [None] * COLUMNS)
        cleared += 1
    return cleared


def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                ##La dimensione è GRID_SIZE × GRID_SIZE
                pygame.draw.rect(surface, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)
                #Disegna un bordo nero spesso 2 pixel sopra il rettangolo precedente
            else:
                pygame.draw.rect(surface, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                #Disegna solo un bordo grigio sottile (1 pixel) per celle vuote


def draw_piece(surface, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, piece.color,
                                 ((piece.x + x) * GRID_SIZE, (piece.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                                #surface: dove viene disegnata la cella
                                #piece.x + x: posizione orizzontale del blocco sul campo
                                #piece.y + y: posizione verticale.
                                #Queste vengono moltiplicate per GRID_SIZE per convertire da coordinate di griglia a pixel sullo schermo. 
                pygame.draw.rect(surface, BLACK,
                                 ((piece.x + x) * GRID_SIZE, (piece.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)
                                 #Stesse coordinate e dimensioni di prima.
                                #Disegna un bordo nero spesso 2 pixel attorno alla cella colorata.
                                #Serve per evidenziare i contorni del pezzo e renderlo più visibile sul campo.


def draw_next_pieces(surface, next_pieces):
    for i, piece in enumerate(next_pieces):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, piece.color, (
                        NEXT_PIECES_POS[0] + x * GRID_SIZE, NEXT_PIECES_POS[1] + y * GRID_SIZE + i * 80,
                        GRID_SIZE, GRID_SIZE))


def draw_text(surface, text, position, size=30, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


def game_over_animation(surface):
    pygame.mixer.music.stop()
    pygame.mixer.Sound("gameover.mp3").play()
    for i in range(255, 0, -5):
        #Riempie tutto lo surface con un colore rosso con intensità i.
        #Man mano che i diminuisce, il rosso si scurisce
        surface.fill((i, 0, 0))
        draw_text(surface, "GAME OVER", (WIDTH // 4, HEIGHT // 2), 50, WHITE)
        pygame.display.flip()
        pygame.time.delay(50)


def play_music():
    pygame.mixer.music.load("Tetris.mp3")
    pygame.mixer.music.play(-1)


def calculate_score(lines):
    if lines == 1:
        return 100
    elif lines == 2:
        return 300
    elif lines == 3:
        return 500
    elif lines >= 4:
        return 800
    return 0


def game(mode):
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH + 150, HEIGHT))
    clock = pygame.time.Clock()
    #crea una griglia bidimensionale (lista di liste) di dimensioni ROWS × COLUMNS, inizializzata con None in ogni cella.
    grid = [[None] * COLUMNS for _ in range(ROWS)]

    current_piece = Piece()
    next_pieces = [Piece(), Piece()]
    drop_time = 0
    running = True
    score = 0
    level = 0
    lines_cleared = 0
    speed = 500
    muted = False
    key_down = False

    play_music()

    while running:
        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_piece(screen, current_piece)
        draw_next_pieces(screen, next_pieces)
        draw_text(screen, f"Score: {score}", (WIDTH + 10, HEIGHT - 120), 24)

        if mode == "levels":
            draw_text(screen, f"Livello: {level + 1}", (WIDTH + 10, HEIGHT - 90), 24)
        
        #Tasto per mutare la musica
        mute_color = (0, 200, 0) if not muted else (200, 0, 0) # per scegliere un colore in base allo stato di muted
        mute_text = "Mute" if not muted else "Unmute"
        mute_rect = pygame.Rect(WIDTH + 30, 10, 90, 35) # crea il rettangolo del tasto mute  
        pygame.draw.rect(screen, mute_color, mute_rect, border_radius=10) # lo disegna sullo schermo
        draw_text(screen, mute_text, (mute_rect.x + 10, mute_rect.y + 5), 24, WHITE)

        pygame.display.flip() # aggiorna i cambiamenti

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(grid, current_piece, -1):
                    current_piece.x -= 1
                elif event.key == pygame.K_RIGHT and not check_collision(grid, current_piece, 1):
                    current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    key_down = True
                elif event.key == pygame.K_UP:
                    rotated = Piece(current_piece.shape)
                    rotated.x, rotated.y = current_piece.x, current_piece.y
                    rotated.rotate()
                    if not check_collision(grid, rotated):
                        current_piece.shape = rotated.shape
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    key_down = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mute_rect.collidepoint(event.pos):
                    muted = not muted
                    pygame.mixer.music.set_volume(0 if muted else 1)

        current_speed = speed
        if mode == "classic":
            current_speed = max(100, speed - (score // 500) * 25)
        elif mode == "levels":
            current_speed = max(100, 500 - level * 35)

        if pygame.time.get_ticks() - drop_time > (current_speed // 5 if key_down else current_speed):
            drop_time = pygame.time.get_ticks()
            if not check_collision(grid, current_piece, 0, 1):
                current_piece.y += 1
            else:
                merge_piece(grid, current_piece)
                cleared = clear_lines(grid)
                score += calculate_score(cleared)
                lines_cleared += cleared

                current_piece = next_pieces.pop(0)
                next_pieces.append(Piece())

                if check_collision(grid, current_piece):
                    game_over_animation(screen)
                    running = False

                if mode == "levels" and lines_cleared >= LEVEL_LINE_GOAL:
                    level += 1
                    lines_cleared = 0
                    if level == MAX_LEVEL:
                        draw_text(screen, "HAI VINTO!", (WIDTH // 4, HEIGHT // 2), 50, WHITE)
                        pygame.display.flip()
                        pygame.time.delay(3000)
                        running = False

        clock.tick(30)
    pygame.quit()
    sys.exit()


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Tetris più meglio")
    font = pygame.font.Font("Pixelated.ttf", 30)
    background = pygame.transform.scale(pygame.image.load("titlebg.webp"), (500, 500))
    pygame.mixer.music.load("titlescreen.mp3")
    pygame.mixer.music.play(-1)

    buttons = {
        "classica": pygame.Rect(150, 300, 200, 40),
        "levels": pygame.Rect(150, 360, 200, 40)
    }

    while True:
        screen.blit(background, (0, 0))
        for label, rect in buttons.items():
            pygame.draw.rect(screen, (100, 100, 255), rect, border_radius=10)
            text = font.render(f"Modalità {label}", True, WHITE)
            screen.blit(text, (rect.x + 15, rect.y + 5))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["classica"].collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    game("classic")
                elif buttons["levels"].collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    game("levels")


if __name__ == "__main__":
    main_menu()
