import pygame
import math


pygame.init()


WIDTH, HEIGHT = 1000, 750
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pulo Gravitacional")


G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100


WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)


BG = pygame.transform.scale(pygame.image.load("background.jpeg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("planeta.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))
SHIP = pygame.transform.scale(pygame.image.load("nave.png"), (OBJ_SIZE * 8, OBJ_SIZE * 8))

font = pygame.font.SysFont("Arial", 18)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        rect = PLANET.get_rect(center=(self.x, self.y))
        win.blit(PLANET, rect)

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.trajectory = []

    def move(self, planet):
        dx = planet.x - self.x
        dy = planet.y - self.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return

        # Cálculo da força gravitacional
        force = (G * self.mass * planet.mass) / distance ** 2

        # Direção da força
        angle = math.atan2(dy, dx)
        acceleration = force / self.mass
        acc_x = acceleration * math.cos(angle)
        acc_y = acceleration * math.sin(angle)

        # Método de Euler
        self.vel_x += acc_x
        self.vel_y += acc_y
        self.x += self.vel_x
        self.y += self.vel_y

        self.trajectory.append((int(self.x), int(self.y)))
        if len(self.trajectory) > 300:
            self.trajectory.pop(0)

    def draw(self):
        if len(self.trajectory) > 1:
            pygame.draw.lines(win, WHITE, False, self.trajectory, 1)
        
        angle = math.degrees(math.atan2(-self.vel_y, self.vel_x))  
        rotated_image = pygame.transform.rotate(SHIP, angle)
        new_rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))

        win.blit(rotated_image, new_rect)

def create_ship(location, mouse, mass):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, mass)
    return obj

def draw_mass_controls(planet_mass, ship_mass):
    pygame.draw.rect(win, GRAY, (10, 10, 200, 60))
    text1 = font.render(f"Planet Mass: {planet_mass}", True, BLACK)
    text2 = font.render(f"Ship Mass: {ship_mass}", True, BLACK)
    win.blit(text1, (15, 15))
    win.blit(text2, (15, 35))

def main():
    clock = pygame.time.Clock()
    running = True

    planet_mass = 100
    ship_mass = 5

    planet = Planet(WIDTH // 2, HEIGHT // 2, planet_mass)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    planet_mass += 100
                    planet.mass = planet_mass
                elif event.key == pygame.K_DOWN:
                    planet_mass = max(10, planet_mass - 100)
                    planet.mass = planet_mass
                elif event.key == pygame.K_RIGHT:
                    ship_mass += 10
                elif event.key == pygame.K_LEFT:
                    ship_mass = max(1, ship_mass - 10)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos, ship_mass)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        # Fundo
        win.blit(BG, (0, 0))
        draw_mass_controls(planet_mass, ship_mass)

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, WHITE, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.move(planet)
            obj.draw()
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.hypot(obj.x - planet.x, obj.y - planet.y) <= PLANET_SIZE
            if off_screen or collided:
                objects.remove(obj)
        planet.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
