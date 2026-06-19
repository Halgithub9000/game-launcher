import os
import sys
import time
import subprocess
import pygame

# --------------------------------------------------
# Configuración
# --------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = "/home/cerebrino/consola"
ASSETS_DIR = os.path.join("assets")

GAMES = [
    {
        "title": "ASTRO REHAB",
        "subtitle": "Aventura / Plataformas",
        "command": ["python3", os.path.join(BASE_DIR, "AstroRehab", "astrorehab", "main.py")],
        "image": os.path.join(ASSETS_DIR, "astrorehab.jpg"),
        "color": (70, 90, 140),
    },
    {
        "title": "SURFER REHAB",
        "subtitle": "Puzzle / Arcade",
        "command": ["python3", os.path.join(BASE_DIR, "SurferRehab", "main.py")],
        "image": os.path.join(ASSETS_DIR, "surferrehab.jpg"),
        "color": (140, 80, 90),
    },
]

FPS = 60
MOVE_COOLDOWN_MS = 180
CONFIRM_COOLDOWN_MS = 250

COLOR_BG = (16, 18, 24)
COLOR_PANEL = (28, 30, 38)
COLOR_CARD = (45, 48, 60)
COLOR_TEXT = (245, 245, 245)
COLOR_SUBTEXT = (170, 175, 185)
COLOR_HIGHLIGHT = (255, 210, 90)
COLOR_DARK = (8, 10, 14)
COLOR_EXIT = (130, 60, 60)
COLOR_ERROR = (180, 70, 70)

CARD_W = 320
CARD_H = 340
CARD_SPACING = 40
CARD_RADIUS = 18

# --------------------------------------------------
# Utilidades
# --------------------------------------------------


def load_image(path, size=None):
    if not os.path.exists(path):
        return None
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.smoothscale(image, size)
        return image
    except Exception:
        return None


def draw_text(surface, text, font, color, center=None, topleft=None):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center is not None:
        rect.center = center
    elif topleft is not None:
        rect.topleft = topleft
    surface.blit(img, rect)
    return rect


def draw_round_rect(surface, rect, color, radius, width=0):
    pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)

# --------------------------------------------------
# Launcher
# --------------------------------------------------


class Launcher:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Launcher Arcade")

        self.clock = pygame.time.Clock()
        self.running = True

        self.title_font = pygame.font.SysFont("dejavusans", 46, bold=True)
        self.subtitle_font = pygame.font.SysFont("dejavusans", 24)
        self.card_title_font = pygame.font.SysFont("dejavusans", 32, bold=True)
        self.card_subtitle_font = pygame.font.SysFont("dejavusans", 22)
        self.info_font = pygame.font.SysFont("dejavusans", 20)
        self.loading_font = pygame.font.SysFont("dejavusans", 34, bold=True)
        self.error_font = pygame.font.SysFont("dejavusans", 24, bold=True)
        self.error_small_font = pygame.font.SysFont("dejavusans", 18)

        self.background = load_image(
            os.path.join(ASSETS_DIR, "fondo.png"),
            size=(self.width, self.height)
        )

        self.images = []
        for game in GAMES:
            self.images.append(load_image(
                game["image"], size=(CARD_W - 32, 180)))

        self.selected = 0
        self.last_move_time = 0
        self.last_confirm_time = 0

        self.joysticks = []
        self.init_joysticks()

    def init_joysticks(self):
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            js = pygame.joystick.Joystick(i)
            js.init()
            self.joysticks.append(js)

    def can_move(self):
        now = pygame.time.get_ticks()
        if now - self.last_move_time >= MOVE_COOLDOWN_MS:
            self.last_move_time = now
            return True
        return False

    def can_confirm(self):
        now = pygame.time.get_ticks()
        if now - self.last_confirm_time >= CONFIRM_COOLDOWN_MS:
            self.last_confirm_time = now
            return True
        return False

    def move_left(self):
        if self.can_move():
            self.selected = (self.selected - 1) % (len(GAMES) + 1)

    def move_right(self):
        if self.can_move():
            self.selected = (self.selected + 1) % (len(GAMES) + 1)

    def confirm(self):
        if not self.can_confirm():
            return

        if self.selected < len(GAMES):
            self.show_loading(GAMES[self.selected]["title"])
            self.launch_game(self.selected)
        else:
            self.running = False

    def back(self):
        self.running = False

    def show_loading(self, game_title):
        self.draw()
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        box = pygame.Rect(0, 0, 420, 140)
        box.center = (self.width // 2, self.height // 2)
        draw_round_rect(self.screen, box, COLOR_PANEL, 18)
        draw_round_rect(self.screen, box, COLOR_HIGHLIGHT, 18, width=3)

        draw_text(
            self.screen,
            "Cargando...",
            self.loading_font,
            COLOR_TEXT,
            center=(self.width // 2, self.height // 2 - 20)
        )
        draw_text(
            self.screen,
            game_title,
            self.info_font,
            COLOR_SUBTEXT,
            center=(self.width // 2, self.height // 2 + 25)
        )

        pygame.display.flip()
        pygame.time.wait(350)

    def show_error(self, title, detail):
        self.draw()
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))

        box = pygame.Rect(0, 0, 760, 220)
        box.center = (self.width // 2, self.height // 2)
        draw_round_rect(self.screen, box, COLOR_PANEL, 18)
        draw_round_rect(self.screen, box, COLOR_ERROR, 18, width=3)

        draw_text(
            self.screen,
            title,
            self.error_font,
            COLOR_TEXT,
            center=(self.width // 2, self.height // 2 - 55)
        )

        detail_text = str(detail) if detail else "Error desconocido"
        if len(detail_text) > 90:
            detail_text = detail_text[:87] + "..."

        draw_text(
            self.screen,
            detail_text,
            self.error_small_font,
            COLOR_SUBTEXT,
            center=(self.width // 2, self.height // 2 - 10)
        )

        draw_text(
            self.screen,
            "Volviendo al Menú ...",
            self.error_small_font,
            COLOR_HIGHLIGHT,
            center=(self.width // 2, self.height // 2 + 45)
        )

        pygame.display.flip()
        pygame.time.wait(2500)

    def relaunch_pygame(self):
        pygame.init()
        pygame.font.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Launcher Arcade")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("dejavusans", 46, bold=True)
        self.subtitle_font = pygame.font.SysFont("dejavusans", 24)
        self.card_title_font = pygame.font.SysFont("dejavusans", 32, bold=True)
        self.card_subtitle_font = pygame.font.SysFont("dejavusans", 22)
        self.info_font = pygame.font.SysFont("dejavusans", 20)
        self.loading_font = pygame.font.SysFont("dejavusans", 34, bold=True)
        self.error_font = pygame.font.SysFont("dejavusans", 24, bold=True)
        self.error_small_font = pygame.font.SysFont("dejavusans", 18)

        self.background = load_image(
            os.path.join(ASSETS_DIR, "fondo.png"),
            size=(self.width, self.height)
        )

        self.images = []
        for game in GAMES:
            self.images.append(load_image(
                game["image"], size=(CARD_W - 32, 180)))

        self.init_joysticks()

    def launch_game(self, game_index):
        command = GAMES[game_index]["command"]

        target_script = command[-1] if command else None
        if not target_script or not os.path.exists(target_script):
            self.show_error("No se pudo abrir el juego",
                            f"Archivo no encontrado: {target_script}")
            return

        game_cwd = os.path.dirname(target_script)
        error_message = None

        pygame.display.quit()
        pygame.quit()

        try:
            process = subprocess.Popen(
                command,
                cwd=game_cwd
            )
            return_code = process.wait()

            if return_code != 0:
                error_message = f"El juego terminó con código {return_code}"

        except Exception as e:
            error_message = str(e)

        self.relaunch_pygame()

        if error_message:
            self.show_error("Error al ejecutar el juego", error_message)

    def handle_keydown(self, key):
        if key in (pygame.K_LEFT, pygame.K_a):
            self.move_left()
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.move_right()
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self.confirm()
        elif key == pygame.K_ESCAPE:
            self.back()

    def handle_joy_axis(self, axis, value):
        if axis == 0:
            if value <= -0.8:
                self.move_left()
            elif value >= 0.8:
                self.move_right()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

            elif event.type == pygame.JOYHATMOTION:
                hat_x, _ = event.value
                if hat_x == -1:
                    self.move_left()
                elif hat_x == 1:
                    self.move_right()

            elif event.type == pygame.JOYAXISMOTION:
                self.handle_joy_axis(event.axis, event.value)

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    self.confirm()
                elif event.button == 1:
                    self.back()

            elif event.type == pygame.JOYDEVICEADDED:
                self.init_joysticks()

            elif event.type == pygame.JOYDEVICEREMOVED:
                self.init_joysticks()

    def draw_background(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
            overlay = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill(COLOR_BG)

    def draw_game_card(self, x, y, game, image, selected):
        shadow = pygame.Rect(x + 8, y + 8, CARD_W, CARD_H)
        draw_round_rect(self.screen, shadow, (0, 0, 0), CARD_RADIUS)

        card = pygame.Rect(x, y, CARD_W, CARD_H)
        draw_round_rect(self.screen, card,
                        game["color"] if selected else COLOR_CARD, CARD_RADIUS)

        border = COLOR_HIGHLIGHT if selected else (85, 90, 100)
        draw_round_rect(self.screen, card, border, CARD_RADIUS, width=4)

        image_rect = pygame.Rect(x + 16, y + 16, CARD_W - 32, 180)
        draw_round_rect(self.screen, image_rect, COLOR_DARK, 12)

        if image:
            img_rect = image.get_rect(center=image_rect.center)
            self.screen.blit(image, img_rect)
        else:
            draw_text(
                self.screen,
                "Sin imagen",
                self.card_subtitle_font,
                COLOR_SUBTEXT,
                center=image_rect.center
            )

        draw_text(
            self.screen,
            game["title"],
            self.card_title_font,
            COLOR_TEXT,
            center=(x + CARD_W // 2, y + 235)
        )

        draw_text(
            self.screen,
            game["subtitle"],
            self.card_subtitle_font,
            COLOR_SUBTEXT,
            center=(x + CARD_W // 2, y + 275)
        )

        if selected:
            draw_text(
                self.screen,
                "ENTER para jugar",
                self.info_font,
                COLOR_HIGHLIGHT,
                center=(x + CARD_W // 2, y + 312)
            )

    def draw_exit_card(self, x, y, selected):
        shadow = pygame.Rect(x + 8, y + 8, CARD_W, CARD_H)
        draw_round_rect(self.screen, shadow, (0, 0, 0), CARD_RADIUS)

        card = pygame.Rect(x, y, CARD_W, CARD_H)
        draw_round_rect(self.screen, card,
                        COLOR_EXIT if selected else COLOR_CARD, CARD_RADIUS)

        border = COLOR_HIGHLIGHT if selected else (85, 90, 100)
        draw_round_rect(self.screen, card, border, CARD_RADIUS, width=4)

        icon_rect = pygame.Rect(x + 16, y + 16, CARD_W - 32, 180)
        draw_round_rect(self.screen, icon_rect, COLOR_DARK, 12)

        draw_text(
            self.screen,
            "SALIR",
            self.title_font,
            COLOR_TEXT,
            center=icon_rect.center
        )

        draw_text(
            self.screen,
            "Cerrar launcher",
            self.card_title_font,
            COLOR_TEXT,
            center=(x + CARD_W // 2, y + 245)
        )

        draw_text(
            self.screen,
            "Volver a Openbox",
            self.card_subtitle_font,
            COLOR_SUBTEXT,
            center=(x + CARD_W // 2, y + 282)
        )

        if selected:
            draw_text(
                self.screen,
                "ENTER para salir",
                self.info_font,
                COLOR_HIGHLIGHT,
                center=(x + CARD_W // 2, y + 312)
            )

    def draw_cards(self):
        total_items = len(GAMES) + 1
        total_width = total_items * CARD_W + (total_items - 1) * CARD_SPACING
        start_x = (self.width - total_width) // 2
        y = (self.height - CARD_H) // 2 + 30

        for i, game in enumerate(GAMES):
            x = start_x + i * (CARD_W + CARD_SPACING)
            self.draw_game_card(x, y, game, self.images[i], self.selected == i)

        exit_index = len(GAMES)
        exit_x = start_x + exit_index * (CARD_W + CARD_SPACING)
        self.draw_exit_card(exit_x, y, self.selected == exit_index)

    def draw_status(self):
        status = "Control por teclado / Bluetooth HID compatible"
        draw_text(
            self.screen,
            status,
            self.info_font,
            COLOR_SUBTEXT,
            center=(self.width // 2, 105)
        )

    def draw_footer(self):
        footer = "Izq/Der o A/D para navegar · Enter/Espacio para aceptar · Esc para salir"
        draw_text(
            self.screen,
            footer,
            self.info_font,
            COLOR_SUBTEXT,
            center=(self.width // 2, self.height - 35)
        )

    def draw(self):
        self.draw_background()

        draw_text(
            self.screen,
            "Mis Juegos",
            self.title_font,
            COLOR_TEXT,
            center=(self.width // 2, 60)
        )

        self.draw_status()
        self.draw_cards()
        self.draw_footer()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Launcher().run()
