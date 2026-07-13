import pygame
import random
import time
import sys
import math
import os

pygame.init()
WIDTH, HEIGHT = 720, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Memory Game")
clock = pygame.time.Clock()

FONT_BIG = pygame.font.SysFont("century gothic", 56, True)
FONT_MED = pygame.font.SysFont("century gothic", 36, True)
FONT = pygame.font.SysFont("century gothic", 26)
FONT_SMALL = pygame.font.SysFont("century gothic", 22)

COLORS = [(231, 76, 60), (46, 204, 113), (52, 152, 219), (241, 196, 15),
          (155, 89, 182), (26, 188, 156), (230, 126, 34), (149, 165, 166)]

BG_TOP = (30, 30, 60)
BG_BOTTOM = (10, 10, 25)

background_img = None
print("=" * 50)
print("Looking for background image...")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")
print("=" * 50)

try:
    for img_file in ["background.jpg", "background.png", "background.jpeg", "ssn.jpg", "college.jpg", "college.png"]:
        full_path = os.path.join(os.getcwd(), img_file)
        if os.path.exists(img_file):
            print(f"✓ Found image: {img_file}")
            background_img = pygame.image.load(img_file)
            background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
            print(f"✓ Successfully loaded: {img_file}")
            break
    if not background_img:
        print("✗ No background image found. Using gradient instead.")
        print("✓ Place your image (background.jpg, ssn.jpg, or college.jpg) in the project folder.")
except Exception as e:
    print(f"✗ Error loading background: {e}")
    print("✓ Using gradient instead.")


def draw_gradient():
    if background_img:
        screen.blit(background_img, (0, 0))
        # Add brighter semi-transparent overlay so text is visible
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(220)  # Increased from 180 to 220
        overlay.fill((15, 15, 35))  # Darker overlay for better contrast
        screen.blit(overlay, (0, 0))
    else:
        for y in range(HEIGHT):
            r = BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * y // HEIGHT
            g = BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * y // HEIGHT
            b = BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * y // HEIGHT
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))


def glow_text(text, font, x, y):
    surf = font.render(text, True, (100, 180, 255))
    screen.blit(surf, surf.get_rect(center=(x, y)))


def button(rect, text, mouse, pressed=False):
    if pressed:
        color = (120, 200, 255)
        border_color = (200, 255, 255)
    elif rect.collidepoint(mouse):
        color = (100, 180, 255)
        border_color = (255, 255, 100)
    else:
        color = (70, 100, 180)
        border_color = (150, 150, 200)

    # Draw main button
    pygame.draw.rect(screen, color, rect, border_radius=25)
    pygame.draw.rect(screen, border_color, rect, 4, border_radius=25)

    # Draw text
    text_surf = FONT.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


def input_name_screen():
    name = ""
    while True:
        draw_gradient()
        glow_text("Enter Your Name", FONT_BIG, WIDTH // 2, 180)
        t = FONT.render(name if name else "Tap to type...", True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=(WIDTH // 2, 300)))
        mouse = pygame.mouse.get_pos()
        ok = pygame.Rect(235, 380, 250, 70)
        button(ok, "CONTINUE", mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12:
                    name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ok.collidepoint(mouse) and len(name) > 0:
                    return name
        pygame.display.update()
        clock.tick(60)


def show_tutorial():
    while True:
        draw_gradient()
        glow_text("How to Play", FONT_BIG, WIDTH // 2, 60)

        instructions = [
            "1. Click any tile to reveal color",
            "2. Click another tile to find match",
            "3. See both colors at same time!",
            "4. Match all pairs before time ends",
            "5. Score: +5 per match",
            "",
            "EASY: 4x4, 40 sec",
            "MEDIUM: 6x6, 60 sec",
            "HARD: 8x8, 80 sec"
        ]

        y = 150
        for instruction in instructions:
            if instruction == "":
                y += 15
                continue
            t = FONT_SMALL.render(instruction, True, (200, 220, 255))
            screen.blit(t, (60, y))
            y += 40

        mouse = pygame.mouse.get_pos()
        back = pygame.Rect(235, 600, 250, 70)
        button(back, "BACK", mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(mouse):
                    return

        pygame.display.update()
        clock.tick(60)


def show_about():
    while True:
        draw_gradient()
        glow_text("About Game", FONT_BIG, WIDTH // 2, 60)

        about_text = [
            "Color Memory Game v2.0",
            "",
            "Developers:",
            "AKSHAYA SIVAGURU",
            "HARSHATH BALA G S",
            "JOSHITHA SHRI S",
            "",
            "A fun memory matching game",
            "Test your memory skills!"
        ]

        y = 150
        for text in about_text:
            if text == "":
                y += 15
                continue
            color = (150, 200,
                     255) if "Developer" in text or "AKSHAYA" in text or "HARSHATH" in text or "JOSHITHA" in text else (
                200, 220, 255)
            t = FONT_SMALL.render(text, True, color)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, y))
            y += 38

        mouse = pygame.mouse.get_pos()
        back = pygame.Rect(235, 620, 250, 70)
        button(back, "BACK", mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(mouse):
                    return

        pygame.display.update()
        clock.tick(60)


def show_statistics():
    if not os.path.exists("leaderboard.txt"):
        games_played = 0
        best_score = 0
        avg_score = 0
    else:
        with open("leaderboard.txt", "r") as f:
            scores = [int(line.split(",")[1]) for line in f if "," in line]
        games_played = len(scores)
        best_score = max(scores) if scores else 0
        avg_score = sum(scores) // len(scores) if scores else 0

    while True:
        draw_gradient()
        glow_text("Statistics", FONT_BIG, WIDTH // 2, 100)

        stats_text = [
            f"Games Played: {games_played}",
            f"Best Score: {best_score}",
            f"Average Score: {avg_score}",
        ]

        y = 250
        for text in stats_text:
            t = FONT_MED.render(text, True, (100, 255, 100))
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, y))
            y += 80

        mouse = pygame.mouse.get_pos()
        back = pygame.Rect(235, 620, 250, 70)
        button(back, "BACK", mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(mouse):
                    return

        pygame.display.update()
        clock.tick(60)


def show_settings():
    while True:
        draw_gradient()
        glow_text("Settings", FONT_BIG, WIDTH // 2, 120)

        mouse = pygame.mouse.get_pos()
        clear_btn = pygame.Rect(235, 280, 250, 70)
        back = pygame.Rect(235, 400, 250, 70)

        button(clear_btn, "CLEAR SCORES", mouse)
        button(back, "BACK", mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if clear_btn.collidepoint(mouse):
                    if os.path.exists("leaderboard.txt"):
                        os.remove("leaderboard.txt")
                elif back.collidepoint(mouse):
                    return

        pygame.display.update()
        clock.tick(60)


def show_game_modes():
    while True:
        draw_gradient()
        glow_text("Game Modes", FONT_BIG, WIDTH // 2, 80)

        mouse = pygame.mouse.get_pos()
        classic = pygame.Rect(235, 180, 250, 55)
        speed = pygame.Rect(235, 250, 250, 55)
        zen = pygame.Rect(235, 320, 250, 55)
        back = pygame.Rect(235, 620, 250, 70)

        button(classic, "CLASSIC MODE", mouse)
        button(speed, "SPEED MODE", mouse)
        button(zen, "ZEN MODE", mouse)
        button(back, "BACK", mouse)

        # Show mode descriptions with better spacing
        desc_y = 410
        desc_text = [
            "CLASSIC: Standard game with timer",
            "SPEED: Faster tiles, shorter time",
            "ZEN: No timer, play at your pace"
        ]
        for text in desc_text:
            t = FONT_SMALL.render(text, True, (150, 200, 255))
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, desc_y))
            desc_y += 32

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if classic.collidepoint(mouse):
                    return "classic"
                elif speed.collidepoint(mouse):
                    return "speed"
                elif zen.collidepoint(mouse):
                    return "zen"
                elif back.collidepoint(mouse):
                    return None

        pygame.display.update()
        clock.tick(60)


def show_about():
    while True:
        draw_gradient()
        glow_text("About Game", FONT_BIG, WIDTH // 2, 100)

        about_text = [
            "Color Memory Game v2.0",
            "",
            "Developers:",
            "AKSHAYA SIVAGURU",
            "HARSHATH BALA G S",
            "JOSHITHA SHRI S",
            "",
            "A fun memory matching game",
            "Test your memory skills!",
            "",
            "Features:",
            "- 3 Difficulty Levels",
            "- High Score Leaderboard",
            "- Beautiful Backgrounds"
        ]

        y = 160
        for text in about_text:
            color = (150, 200, 255) if text else (100, 100, 100)
            t = FONT_SMALL.render(text, True, color)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, y))
            y += 35

        mouse = pygame.mouse.get_pos()
        back = pygame.Rect(235, 620, 250, 70)
        button(back, "BACK", mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(mouse):
                    return

        pygame.display.update()
        clock.tick(60)


def save_score(name, score):
    with open("leaderboard.txt", "a") as f:
        f.write(f"{name},{score}\n")


def load_leaderboard():
    if not os.path.exists("leaderboard.txt"):
        return []
    arr = []
    with open("leaderboard.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 2:
                continue
            name, score = parts
            if score.isdigit():
                arr.append((name, int(score)))
    arr.sort(key=lambda x: x[1], reverse=True)
    return arr[:10]


def show_leaderboard():
    data = load_leaderboard()
    while True:
        draw_gradient()
        glow_text("Leaderboard", FONT_BIG, WIDTH // 2, 80)
        if len(data) == 0:
            t = FONT.render("Be the first one to conquer!", True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=(WIDTH // 2, 300)))
        else:
            y = 150
            # Draw header with proper spacing
            rank_h = FONT_SMALL.render("RANK", True, (255, 200, 100))
            screen.blit(rank_h, (60, y))

            name_h = FONT_SMALL.render("NAME", True, (255, 200, 100))
            screen.blit(name_h, (120, y))

            score_h = FONT_SMALL.render("SCORE", True, (255, 200, 100))
            screen.blit(score_h, (600, y))

            y += 45

            # Draw separator line
            pygame.draw.line(screen, (150, 150, 150), (60, y), (660, y), 2)
            y += 25

            for i, (n, s) in enumerate(data):
                # Separate rank, name, and score with fixed positions
                rank_text = f"{i + 1:2d}."
                name_text = f"{n[:13]:<13}"
                score_text = f"{s:>5d}"

                # Draw each part at fixed x position
                rank = FONT_SMALL.render(rank_text, True, (100, 255, 100))
                screen.blit(rank, (60, y))

                name = FONT_SMALL.render(name_text, True, (200, 255, 200))
                screen.blit(name, (120, y))

                score = FONT_SMALL.render(score_text, True, (100, 200, 255))
                screen.blit(score, (600, y))  # Moved to right corner

                y += 45

        mouse = pygame.mouse.get_pos()
        back = pygame.Rect(235, 620, 250, 70)
        button(back, "BACK", mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(mouse):
                    return
        pygame.display.update()
        clock.tick(60)


def main_menu():
    while True:
        draw_gradient()
        glow_text("Color Memory Game", FONT_BIG, WIDTH // 2, 80)
        mouse = pygame.mouse.get_pos()
        play = pygame.Rect(235, 180, 250, 55)
        lead = pygame.Rect(235, 245, 250, 55)
        stats = pygame.Rect(235, 310, 250, 55)
        tut = pygame.Rect(235, 375, 250, 55)
        settings = pygame.Rect(235, 440, 250, 55)
        about = pygame.Rect(235, 505, 250, 55)
        button(play, "PLAY", mouse)
        button(lead, "LEADERBOARD", mouse)
        button(stats, "STATISTICS", mouse)
        button(tut, "TUTORIAL", mouse)
        button(settings, "SETTINGS", mouse)
        button(about, "ABOUT", mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.collidepoint(mouse):
                    mode = show_game_modes()
                    if mode:
                        return mode
                elif lead.collidepoint(mouse):
                    show_leaderboard()
                elif stats.collidepoint(mouse):
                    show_statistics()
                elif tut.collidepoint(mouse):
                    show_tutorial()
                elif settings.collidepoint(mouse):
                    show_settings()
                elif about.collidepoint(mouse):
                    show_about()
        pygame.display.update()
        clock.tick(60)


def difficulty_menu(mode="classic"):
    while True:
        draw_gradient()
        glow_text("Select Difficulty", FONT_BIG, WIDTH // 2, 80)
        mouse = pygame.mouse.get_pos()
        easy = pygame.Rect(235, 200, 250, 55)
        med = pygame.Rect(235, 280, 250, 55)
        hard = pygame.Rect(235, 360, 250, 55)
        button(easy, "EASY (4x4) 40s", mouse)
        button(med, "MEDIUM (6x6) 60s", mouse)
        button(hard, "HARD (8x8) 80s", mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy.collidepoint(mouse):
                    if mode == "speed":
                        return 4, 25
                    elif mode == "zen":
                        return 4, 999
                    else:
                        return 4, 40
                if med.collidepoint(mouse):
                    if mode == "speed":
                        return 6, 40
                    elif mode == "zen":
                        return 6, 999
                    else:
                        return 6, 60
                if hard.collidepoint(mouse):
                    if mode == "speed":
                        return 8, 50
                    elif mode == "zen":
                        return 8, 999
                    else:
                        return 8, 80
        pygame.display.update()
        clock.tick(60)


def game(grid, limit):
    total = grid * grid
    pool = COLORS * ((total // 2) // len(COLORS) + 1)
    tiles = pool[:total // 2] * 2
    random.shuffle(tiles)
    revealed = [False] * total
    selected = []
    score = 0
    matches = 0
    start = time.time()
    last_tap_time = 0
    match_time = 0

    while True:
        draw_gradient()
        mouse = pygame.mouse.get_pos()
        left = int(limit - (time.time() - start))
        if left <= 0:
            return score

        exit_btn = pygame.Rect(20, 20, 150, 50)
        button(exit_btn, "EXIT", mouse)

        size = 110 if grid == 4 else 75 if grid == 6 else 60
        gap = 20
        offx = (WIDTH - (grid * size + (grid - 1) * gap)) // 2
        offy = 100

        if len(selected) == 2 and time.time() - match_time > 1.0:
            if tiles[selected[0]] == tiles[selected[1]]:
                score += 5
                matches += 1
            else:
                revealed[selected[0]] = False
                revealed[selected[1]] = False
            selected = []

        for i in range(total):
            r = i // grid
            c = i % grid
            x = offx + c * (size + gap)
            y = offy + r * (size + gap)
            rect = pygame.Rect(x, y, size, size)

            if revealed[i]:
                pygame.draw.rect(screen, tiles[i], rect, border_radius=15)
                pygame.draw.rect(screen, (255, 255, 200), rect, 3, border_radius=15)
                t = FONT.render("✓", True, (255, 255, 255))
                screen.blit(t, t.get_rect(center=rect.center))
            else:
                is_hovered = rect.collidepoint(mouse)
                base = (140, 140, 180) if is_hovered else (100, 100, 140)
                pygame.draw.rect(screen, base, rect, border_radius=15)
                if is_hovered:
                    pygame.draw.rect(screen, (200, 200, 220), rect, 3, border_radius=15)
                t = FONT.render("?", True, (255, 255, 255))
                screen.blit(t, t.get_rect(center=rect.center))

        screen.blit(FONT.render(f"Score: {score}", True, (100, 255, 100)), (40, 650))
        screen.blit(FONT.render(f"Matches: {matches}/{total // 2}", True, (100, 200, 255)), (220, 650))
        screen.blit(FONT.render(f"Time: {left}s", True, (255, 180, 180) if left < 10 else (255, 255, 100)),
                    (WIDTH - 220, 650))

        if len(selected) == 2:
            status = "Checking..." if tiles[selected[0]] != tiles[selected[1]] else "Match!"
            color = (100, 255, 100) if tiles[selected[0]] == tiles[selected[1]] else (200, 200, 255)
            status_text = FONT_MED.render(status, True, color)
            screen.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, 560))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_time = time.time()
                if current_time - last_tap_time < 0.1:
                    continue
                last_tap_time = current_time

                if exit_btn.collidepoint(mouse):
                    return score

                if len(selected) < 2:
                    for i in range(total):
                        r = i // grid
                        c = i % grid
                        x = offx + c * (size + gap)
                        y = offy + r * (size + gap)
                        if pygame.Rect(x, y, size, size).collidepoint(mouse):
                            if not revealed[i] and not selected.count(i):
                                revealed[i] = True
                                selected.append(i)
                                if len(selected) == 2:
                                    match_time = time.time()

        pygame.display.update()
        clock.tick(60)


while True:
    choice = main_menu()
    mode = choice  # choice is now the mode (classic, speed, zen)

    name = input_name_screen()

    while True:
        grid, time_limit = difficulty_menu(mode)
        final = game(grid, time_limit)
        save_score(name, final)

        game_over = True
        while game_over:
            draw_gradient()
            glow_text("Game Over", FONT_BIG, WIDTH // 2, 160)
            sc = FONT_MED.render(f"{name}'s Score: {final}", True, (100, 255, 100))
            screen.blit(sc, sc.get_rect(center=(WIDTH // 2, 260)))
            mouse = pygame.mouse.get_pos()
            again = pygame.Rect(235, 350, 250, 70)
            lead = pygame.Rect(235, 440, 250, 70)
            back = pygame.Rect(235, 530, 250, 70)
            button(again, "PLAY AGAIN", mouse)
            button(lead, "LEADERBOARD", mouse)
            button(back, "BACK TO MENU", mouse)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if again.collidepoint(mouse):
                        game_over = False
                    elif lead.collidepoint(mouse):
                        show_leaderboard()
                    elif back.collidepoint(mouse):
                        game_over = False
                        break

            pygame.display.update()
            clock.tick(60)

        if event.type == pygame.MOUSEBUTTONDOWN and back.collidepoint(mouse):
            break