import pygame
import sys
import random
import copy

from main import print

# Pygame initialisieren
pygame.init()
# add the Music and fix the volume to 5
pygame.mixer.init()
pygame.mixer.music.load('summer-memories .mp3')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)  # play many times
#  to fix the constants
WIDTH, HEIGHT = 500, 600  # Breite und Höhe des Fensters
GRID_SIZE = 4
# Anzahl der Zellen pro Zeile/Spalte
TILE_SIZE = WIDTH // GRID_SIZE  # Größe eines einzelnen Feldes
FONT_SIZE = 50
SCORE_FONT_SIZE = 30
FONT = pygame.font.Font(None, FONT_SIZE)  # parameter for variables (numbers)
SCORE_FONT = pygame.font.Font(None, SCORE_FONT_SIZE)  # parameter for variables(text , score´s value)
COLORS = {  # library von different colors depending on the values of the numbers
    0: (200, 200, 200), 2: (238, 228, 218), 4: (237, 224, 200),
    8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
    64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97),
    512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46),
}

# Initialisierung des Fensters
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("2048")


def str(value):
    pass


def draw_grid(grid, score, suggestion=None):
    # draw the Game_surface and give it the color (187,173,160)
    #     """
    screen.fill((187, 173, 160))  # Background´s color

    # Score anzeigen
    score_text = SCORE_FONT.render(f"Score:{score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Position des Scores

    # Vorschlag für den besten Zug anzeigen
    suggestion_text = SCORE_FONT.render(f"Best Move: {suggestion if suggestion else 'None'}", True, (255, 255, 255))
    screen.blit(suggestion_text, (10, 40))

    # Parcourir les lignes et les colonnes du tableau
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            value = grid[row][col]  # Wert der aktuellen Kachel
            color = COLORS.get(value, (60, 58, 50))  # Farbe abhängig vom Wert
            # Draw the Game_Space and to check if

            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE + 100, TILE_SIZE, TILE_SIZE))
            if value != 0:  # if there is a number in the Grid
                text = FONT.render(str(value), True, (
                0, 0, 0))  # this variable help us to convert our number in text to make it realess whit a black color
                text_rect = text.get_rect(
                    center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2 + 100))
                screen.blit(text, text_rect)


def spawn_tile(grid):
    """

    """

    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_tiles:  # Nur wenn es freie Tile  gibt
        row, col = random.choice(empty_tiles)  # Wählt eine zufällige freie Zelle
        grid[row][col] = 2 if random.random() < 0.9 else 4  # 90% Wahrscheinlichkeit für 2, 10% für 4


def len(new_row):
    pass


def slide_and_merge(row):
    """


    Führt das Verschieben und Zusammenführen für eine einzelne Reihe durch.
    """
    new_row = [value for value in row if value != 0]  # Entfernt alle Nullen
    score_gain = 0  # Punkte, die durch diesen Zug gewonnen werden
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:  # Wenn zwei nebeneinander liegende Werte gleich sind
            new_row[i] *= 2  # Verdoppelt den Wert
            score_gain += new_row[i]  # Addiert den neuen Wert zu den Punkten
            new_row[i + 1] = 0  # Setzt die zweite Kachel auf 0
    new_row = [value for value in new_row if value != 0]  # Entfernt erneut Nullen
    return new_row + [0] * (GRID_SIZE - len(new_row)), score_gain  # Rückgabe der neuen Reihe und der Punkte


def move(grid, direction):
    """
    Führt eine Bewegung in die angegebene Richtung aus.
    """
    moved = False  # Gibt an, ob sich etwas geändert hat

    score_gain = 0  # Punktegewinn durch den Zug
    if direction in ("LEFT", "RIGHT"):
        for row in grid:
            original = row[:]  # Kopiert die aktuelle Reihe
            new_row, gain = slide_and_merge(row if direction == "LEFT" else row[::-1])
            if direction == "RIGHT":
                new_row.reverse()  # Dreht die Reihe zurück
            row[:] = new_row  # Aktualisiert die Reihe
            score_gain += gain
            moved |= (row != original)  # Prüft, ob sich etwas geändert hat
    elif direction in ("UP", "DOWN"):
        for col in range(GRID_SIZE):
            column = [grid[row][col] for row in range(GRID_SIZE)]  # Spaltenweise Bewegung
            original = column[:]
            new_column, gain = slide_and_merge(column if direction == "UP" else column[::-1])
            if direction == "DOWN":
                new_column.reverse()
            for row in range(GRID_SIZE):
                grid[row][col] = new_column[row]
            score_gain += gain
            moved |= (new_column != original)
    return moved, score_gain


def calculate_merge_value(grid, direction):
    """
    Berechnet den Gesamtwert der Zusammenführungen für eine bestimmte Richtung.
    """
    temp_grid = copy.deepcopy(grid)  # Erstelle eine Kopie des Gitters
    merge_value = 0
    if direction in ("LEFT", "RIGHT"):
        for row in temp_grid:
            _, gain = slide_and_merge(row if direction == "LEFT" else row[::-1])
            merge_value += gain
    elif direction in ("UP", "DOWN"):
        for col in range(GRID_SIZE):
            column = [temp_grid[row][col] for row in range(GRID_SIZE)]
            _, gain = slide_and_merge(column if direction == "UP" else column[::-1])
            merge_value += gain
    return merge_value


def suggest_best_move(grid):
    """
    Gibt die Richtung mit dem höchsten Zusammenführungswert zurück.
    Gibt 'None' zurück, wenn keine Zusammenführungen möglich sind.
    """
    directions = ["LEFT", "RIGHT", "UP", "DOWN"]
    best_move = None
    max_merge_value = 0  # Startwert für den höchsten Zusammenführungswert

    for direction in directions:
        merge_value = calculate_merge_value(grid, direction)
        if merge_value > max_merge_value:
            max_merge_value = merge_value
            best_move = direction

    # Wenn keine Zusammenführungen möglich sind, wird None zurückgegeben
    return best_move if max_merge_value > 0 else None


def range(GRID_SIZE):
    pass


def check_game_over(grid):
    """
    Prüft, ob das Spiel beendet ist (keine Züge mehr möglich).
    """
    for row in grid:
        for value in row:
            if value == 0:
                return False
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 1):
            if grid[row][col] == grid[row][col + 1]:
                return False
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 1):
            if grid[row][col] == grid[row + 1][col]:
                return False
    return True


def check_win(grid):
    """
    Prüft, ob der Spieler gewonnen hat (2048 erreicht wurde).
    """
    for row in grid:
        for value in row:
            if value == 2048:
                pygame.mixer.music.load("summer-memories .mp3")
                pygame.mixer.music.set_volume(500)
                return True
    return False


def main():
    """
    Hauptspielschleife, die   die Logik und das Rendering koordiniert.
    """
    clock = pygame.time.Clock()  # Steuerung der Bildrate
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  # Initialisiert das Gitter
    spawn_tile(grid)  # Fügt zwei Startkacheln hinzu
    spawn_tile(grid)
    score = 0
    won = False

    running = True
    while running:
        suggestion = suggest_best_move(grid)  # Vorschlag für den besten Zug

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Spiel beenden
                running = False
            if event.type == pygame.KEYDOWN and not won:
                direction = None
                if event.key == pygame.K_LEFT:
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"
                elif event.key == pygame.K_UP:
                    direction = "UP"
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"
                if direction:
                    moved, score_gain = move(grid, direction)  # Bewegung ausführen
                    score += score_gain
                    if moved:
                        spawn_tile(grid)  # Neue Kachel hinzufügen
                    if check_win(grid):  # Gewinn überprüfen
                        won = True
                        print("Congratulations, you win!")
                    if check_game_over(grid):  # Verlust überprüfen
                        print("Game Over!")
                        running = False

        draw_grid(grid, score, suggestion)  # Zeichnet das Spielfeld und den Vorschlag
        if won:
            win_text = FONT.render("Congratulations, you win!", True, (255, 255, 255))
            text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(win_text, text_rect)

        pygame.display.flip()  # Aktualisiert den Bildschirm
        clock.tick(30)  # Framerate steuern

    pygame.mixer.music.stop()
    pygame.quit()  # Pygame schließen
    sys.exit()


if __name__ == "__main__":
    main()
