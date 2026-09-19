"""Pygame"""
import os
import random
import pygame
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snek")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (25, 170, 25)

WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BACKGROUND_PIC = pygame.image.load(os.path.join('Assets', 'checkerboard (2).png'))

FPS = 50
SNAKE_WIDTH, SNAKE_HEIGHT = 25, 25

APPLE_COUNT = 10
class Snake(pygame.sprite.Sprite):
    """The snake class."""
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((SNAKE_WIDTH, SNAKE_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = pygame.Vector2(1, 0)
        self.velocity = 25
        self.living = True
        self.body = [self.rect.copy()]
        self.length = 1

    def update(self, tick):
        """Update the snake's position and body segments."""
        if tick % 25 == 0:
            self.rect.x += self.direction.x * self.velocity
            self.rect.y += self.direction.y * self.velocity
            self.body.append(self.rect.copy())
            if len(self.body) > self.length:
                self.body.pop(0)


    def turn(self, new_direction):
        """Turn the snake in a new direction."""
        if new_direction.x != -self.direction.x and new_direction.y != -self.direction.y:
            self.direction = new_direction

    def eat(self):
        """Increase the length of the snake when it eats an apple."""
        self.length += 1

    def alive(self):
        """Check if the snake is alive."""
        return self.living

    def draw(self, surface):
        """Draw the snake on the given surface."""
        color = self.image.get_at((0, 0))
        for segment in self.body[:-1]:
            pygame.draw.rect(surface, color, segment)

        head_rect = self.body[-1]
        head_draw_rect = head_rect.inflate(-4, -4)
        pygame.draw.rect(surface, color, head_draw_rect)

        eye_color = BLACK
        pupil_color = WHITE
        eye_radius = 3

        cx = head_rect.centerx
        cy = head_rect.centery

        if self.direction.x == 1:  # Right
            eye1 = (cx + 4, cy - 5)
            eye2 = (cx + 4, cy + 5)
        elif self.direction.x == -1:  # Left
            eye1 = (cx - 4, cy - 5)
            eye2 = (cx - 4, cy + 5)
        elif self.direction.y == -1:  # Up
            eye1 = (cx - 5, cy - 4)
            eye2 = (cx + 5, cy - 4)
        else:  # Down
            eye1 = (cx - 5, cy + 4)
            eye2 = (cx + 5, cy + 4)

        for eye_pos in (eye1, eye2):
            pygame.draw.circle(surface, pupil_color, eye_pos, eye_radius)
            pygame.draw.circle(surface, eye_color, eye_pos, eye_radius - 1)

class Apple(pygame.sprite.Sprite):
    """The apple class."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((SNAKE_WIDTH, SNAKE_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def respawn(self, snake_bodies=[]):
        """Respawn the apple at a random grid position not occupied by a snake."""
        while True:
            x = random.randint(0, (WIDTH // SNAKE_WIDTH) - 1) * SNAKE_WIDTH
            y = random.randint(0, (HEIGHT // SNAKE_HEIGHT) - 1) * SNAKE_HEIGHT
            self.rect.topleft = (x, y)

            overlap = any(self.rect.colliderect(segment) for segment in snake_bodies)
            if not overlap:
                break


BOARDSIZE = (WIDTH // SNAKE_WIDTH) * (HEIGHT // SNAKE_HEIGHT)
sprites = pygame.sprite.Group()
sprites.add(Snake(BLUE, 400, 300))
sprites.add(Snake(YELLOW, 100, 300))

def get_all_snake_segments():
    """Gather all Rect segments from all active snakes."""
    snake_bodies = []
    for sprite in sprites:
        if isinstance(sprite, Snake):
            snake_bodies.extend(sprite.body)
    return snake_bodies

for _ in range(APPLE_COUNT):
    apple = Apple(0, 0)
    apple.respawn(get_all_snake_segments())
    sprites.add(apple)

def yellow_handle_movement(keys_pressed, yellow):
    """Handle the movement of the yellow snake based on key presses."""
    if keys_pressed[pygame.K_a] and yellow.rect.x > 0:  # LEFT
        yellow.turn(pygame.Vector2(-1, 0))
    if keys_pressed[pygame.K_d] and yellow.rect.x + yellow.rect.width < WIDTH:  # RIGHT
        yellow.turn(pygame.Vector2(1, 0))
    if keys_pressed[pygame.K_w] and yellow.rect.y > 0:  # UP
        yellow.turn(pygame.Vector2(0, -1))
    if keys_pressed[pygame.K_s] and yellow.rect.y + yellow.rect.height < HEIGHT:  # DOWN
        yellow.turn(pygame.Vector2(0, 1))


def red_handle_movement(keys_pressed, red):
    """Handle the movement of the red snake based on key presses."""
    if keys_pressed[pygame.K_LEFT] and red.rect.x > 0:  # LEFT
        red.turn(pygame.Vector2(-1, 0))
    if keys_pressed[pygame.K_RIGHT] and red.rect.x + red.rect.width < WIDTH:  # RIGHT
        red.turn(pygame.Vector2(1, 0))
    if keys_pressed[pygame.K_UP] and red.rect.y > 0:  # UP
        red.turn(pygame.Vector2(0, -1))
    if keys_pressed[pygame.K_DOWN] and red.rect.y + red.rect.height < HEIGHT:  # DOWN
        red.turn(pygame.Vector2(0, 1))

def draw_winner(text):
    """Make big text in the middle of the screen that says who won."""
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def reset_game():
    """Reset the game by clearing the sprites and adding new snakes."""
    global sprites
    sprites.empty()
    sprites.add(Snake(RED, 400, 300))
    sprites.add(Snake(BLUE, 100, 300))
    snake_bodies = get_all_snake_segments()

    for _ in range(APPLE_COUNT):
        apple = Apple(0, 0)
        apple.respawn(snake_bodies)
        sprites.add(apple)

def handle_collision(snake1, snake2):
    """Check if there are collisions."""
    
    # 1. Head-to-Head Collision
    if snake1.rect.colliderect(snake2.rect):
        snake1.living = False
        snake2.living = False

    # 2. Boundary / Wall Collisions (Off-screen check)
    for snake in [snake1, snake2]:
        if (snake.rect.x < 0 or snake.rect.x >= WIDTH or 
            snake.rect.y < 0 or snake.rect.y >= HEIGHT):
            snake.living = False

    # 3. Head colliding with Opponent's Body
    # Test snake1's head against all of snake2's body segments
    for segment in snake2.body:
        if snake1.rect.colliderect(segment):
            snake1.living = False
            break

    # Test snake2's head against all of snake1's body segments
    for segment in snake1.body:
        if snake2.rect.colliderect(segment):
            snake2.living = False
            break

    # 4. Self-Collision (Head colliding with own Tail)
    # Exclude the last segment (self.body[-1]), which is the head itself!
    for snake in [snake1, snake2]:
        for segment in snake.body[:-1]:
            if snake.rect.colliderect(segment):
                snake.living = False
                break

    # 5. Apple Collisions
    all_segments = snake1.body + snake2.body
    for apple in [sprite for sprite in sprites if isinstance(sprite, Apple)]:
        if snake1.rect.colliderect(apple.rect):
            snake1.eat()
            apple.respawn(all_segments)
        elif snake2.rect.colliderect(apple.rect):
            snake2.eat()
            apple.respawn(all_segments)

def main():
    """The main game loop."""
    clock = pygame.time.Clock()
    run = True
    tick = 0
    while run:
        yellow = sprites.sprites()[1]
        red = sprites.sprites()[0]
        clock.tick(FPS)
        tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        if yellow.alive():
            yellow_handle_movement(keys_pressed, yellow)
        if red.alive():
            red_handle_movement(keys_pressed, red)

        handle_collision(red, yellow)

        if not red.alive() and yellow.alive() and yellow.length == BOARDSIZE-1:
            winner_text = "Yellow Wins!"
            draw_winner(winner_text)
            reset_game()
            break

        if not yellow.alive() and red.alive() and red.length == BOARDSIZE-1:
            winner_text = "Red Wins!"
            draw_winner(winner_text)
            reset_game()
            break

        if not red.alive() and not yellow.alive():
            if red.length > yellow.length:
                winner_text = "Red Wins!"
            elif yellow.length > red.length:
                winner_text = "Yellow Wins!"
            else:
                winner_text = "Draw"
            draw_winner(winner_text)
            reset_game()
            break


        sprites.update(tick)
        WIN.blit(BACKGROUND_PIC, (0, 0))
        for sprite in sprites:
            if isinstance(sprite, Snake):
                sprite.draw(WIN)
            else:
                WIN.blit(sprite.image, sprite.rect)
        pygame.display.update()


if __name__ == "__main__":
    main()
