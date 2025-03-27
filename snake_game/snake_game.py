import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')

# Initialize font
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_COUNT//2, GRID_COUNT//2)]
        self.direction = [1, 0]
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
        self.body.insert(0, new_head)

    def check_collision(self):
        head = self.body[0]
        # Check wall collision
        if (head[0] < 0 or head[0] >= GRID_COUNT or 
            head[1] < 0 or head[1] >= GRID_COUNT):
            return True
        
        # Check self collision
        if head in self.body[1:]:
            return True
        
        return False

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def show_title_screen():
    screen.fill(BLACK)
    draw_text("SNAKE GAME", WHITE, WINDOW_SIZE//2, WINDOW_SIZE//3)
    draw_text("Press SPACE to Start", WHITE, WINDOW_SIZE//2, WINDOW_SIZE//2)
    draw_text("Use Arrow Keys to Move", WHITE, WINDOW_SIZE//2, 2*WINDOW_SIZE//3)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def show_game_over_screen(score):
    screen.fill(BLACK)
    draw_text("GAME OVER!", RED, WINDOW_SIZE//2, WINDOW_SIZE//3)
    draw_text(f"Score: {score}", WHITE, WINDOW_SIZE//2, WINDOW_SIZE//2)
    draw_text("Press SPACE to Play Again", WHITE, WINDOW_SIZE//2, 2*WINDOW_SIZE//3)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def main():
    while True:
        show_title_screen()
        
        clock = pygame.time.Clock()
        snake = Snake()
        food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
        score = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.direction != [0, 1]:
                        snake.direction = [0, -1]
                    elif event.key == pygame.K_DOWN and snake.direction != [0, -1]:
                        snake.direction = [0, 1]
                    elif event.key == pygame.K_LEFT and snake.direction != [1, 0]:
                        snake.direction = [-1, 0]
                    elif event.key == pygame.K_RIGHT and snake.direction != [-1, 0]:
                        snake.direction = [1, 0]
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Move snake
            snake.move()

            # Check if snake ate food
            if snake.body[0] == food:
                snake.grow = True
                score += 1
                food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
                while food in snake.body:
                    food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))

            # Check collision
            if snake.check_collision():
                show_game_over_screen(score)
                break

            # Draw everything
            screen.fill(BLACK)
            
            # Draw grid lines
            for x in range(0, WINDOW_SIZE, GRID_SIZE):
                pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, WINDOW_SIZE))
            for y in range(0, WINDOW_SIZE, GRID_SIZE):
                pygame.draw.line(screen, (40, 40, 40), (0, y), (WINDOW_SIZE, y))
            
            # Draw snake
            for i, segment in enumerate(snake.body):
                color = GREEN if i == 0 else (0, 200, 0)  # Different color for head
                pygame.draw.rect(screen, color, 
                               (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, 
                                GRID_SIZE-2, GRID_SIZE-2))
            
            # Draw food
            pygame.draw.rect(screen, RED,
                           (food[0]*GRID_SIZE, food[1]*GRID_SIZE,
                            GRID_SIZE-2, GRID_SIZE-2))

            # Draw score
            draw_text(f"Score: {score}", WHITE, 70, 30)

            # Update display
            pygame.display.flip()
            
            # Control game speed
            clock.tick(10)

if __name__ == "__main__":
    main()
