import pygame
import random
import os

class FlappyBird:
    def __init__(self):
        pygame.init()
        
        # Game Constants
        self.SCREEN_WIDTH = 400
        self.SCREEN_HEIGHT = 600
        self.BIRD_X = 100
        self.BIRD_Y = self.SCREEN_HEIGHT // 2
        self.PIPE_WIDTH = 70
        self.PIPE_GAP = 200
        self.GRAVITY = 0.5
        self.JUMP_STRENGTH = -10
        self.PIPE_SPEED = 4
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 200, 0)
        self.BLUE = (135, 206, 250)
        self.RED = (255, 0, 0)
        
        # Game Setup
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        
        # Load and scale images
        self.load_assets()
        
        # Game State
        self.reset_game()
        
        # Sounds
        self.jump_sound = pygame.mixer.Sound("assets/wing.mp3")
        self.score_sound = pygame.mixer.Sound("assets/point.mp3")
        self.hit_sound = pygame.mixer.Sound("assets/hit.mp3")
        
    def load_assets(self):
        # Create assets directory if it doesn't exist
        if not os.path.exists("assets"):
            os.makedirs("assets")
            
        # Load images with error handling
        try:
            self.bird_img = pygame.image.load("assets/bird.png")
            self.pipe_img = pygame.image.load("assets/pipe.png")
            self.bg_img = pygame.image.load("assets/background.png")
        except pygame.error:
            # Create default shapes if images not found
            self.bird_img = self.create_bird_surface()
            self.pipe_img = self.create_pipe_surface()
            self.bg_img = self.create_background_surface()
            
        # Scale images
        self.bird_img = pygame.transform.scale(self.bird_img, (40, 30))
        self.pipe_img = pygame.transform.scale(self.pipe_img, (self.PIPE_WIDTH, 300))
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
    def create_bird_surface(self):
        surface = pygame.Surface((40, 30))
        surface.fill(self.RED)
        return surface
        
    def create_pipe_surface(self):
        surface = pygame.Surface((self.PIPE_WIDTH, 300))
        surface.fill(self.GREEN)
        return surface
        
    def create_background_surface(self):
        surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        surface.fill(self.BLUE)
        return surface
        
    def reset_game(self):
        self.bird_y = self.BIRD_Y
        self.velocity = 0
        self.pipes = [self.create_pipe()]
        self.score = 0
        self.game_over = False
        self.high_score = self.load_high_score()
        
    def create_pipe(self):
        height = random.randint(100, 400)
        top_pipe = pygame.Rect(self.SCREEN_WIDTH, 0, self.PIPE_WIDTH, height)
        bottom_pipe = pygame.Rect(
            self.SCREEN_WIDTH,
            height + self.PIPE_GAP,
            self.PIPE_WIDTH,
            self.SCREEN_HEIGHT - height - self.PIPE_GAP
        )
        return [top_pipe, bottom_pipe, False]  # False flag for score counting
        
    def draw_pipes(self):
        for pipe in self.pipes:
            # Draw top pipe (flipped)
            pipe_surface = pygame.transform.flip(self.pipe_img, False, True)
            self.screen.blit(pipe_surface, pipe[0])
            # Draw bottom pipe
            self.screen.blit(self.pipe_img, pipe[1])
            
    def draw_bird(self):
        # Rotate bird based on velocity
        angle = max(-30, min(self.velocity * -2, 30))
        rotated_bird = pygame.transform.rotate(self.bird_img, angle)
        self.screen.blit(rotated_bird, (self.BIRD_X, self.bird_y))
        
    def draw_score(self):
        # Current score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # High score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, self.WHITE)
        self.screen.blit(high_score_text, (10, 50))
        
    def draw_game_over(self):
        game_over_text = self.big_font.render("Game Over!", True, self.RED)
        restart_text = self.font.render("Press SPACE to restart", True, self.WHITE)
        
        self.screen.blit(game_over_text, 
            (self.SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
             self.SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
        self.screen.blit(restart_text, 
            (self.SCREEN_WIDTH//2 - restart_text.get_width()//2, 
             self.SCREEN_HEIGHT//2 + 50))
             
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except:
            return 0
            
    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))
            
    def handle_collision(self):
        # Create a smaller hit box for the bird (70% of original size)
        bird_width = 28  # 70% of 40
        bird_height = 21  # 70% of 30
        x_offset = (40 - bird_width) // 2
        y_offset = (30 - bird_height) // 2
        
        bird_rect = pygame.Rect(
            self.BIRD_X + x_offset,
            self.bird_y + y_offset,
            bird_width,
            bird_height
        )
        
        # Ground and ceiling collision with adjusted hitbox
        if self.bird_y + bird_height + y_offset >= self.SCREEN_HEIGHT or self.bird_y + y_offset <= 0:
            if not self.game_over:
                self.game_over = True
                self.hit_sound.play()
            return True
            
        # Pipe collision with adjusted hitbox
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
                if not self.game_over:
                    self.game_over = True
                    self.hit_sound.play()
                return True
        return False
        
    def run(self):
        running = True
        while running:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_over:
                            self.reset_game()
                        else:
                            self.velocity = self.JUMP_STRENGTH
                            self.jump_sound.play()
                            
            if not self.game_over:
                # Bird Physics
                self.velocity += self.GRAVITY
                self.bird_y += self.velocity
                
                # Update Pipes
                for pipe in self.pipes:
                    pipe[0].x -= self.PIPE_SPEED
                    pipe[1].x -= self.PIPE_SPEED
                    
                    # Score counting
                    if not pipe[2] and pipe[0].x < self.BIRD_X:
                        self.score += 1
                        pipe[2] = True
                        self.score_sound.play()
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_high_score()
                
                # Remove off-screen pipes and add new ones
                if self.pipes[0][0].x < -self.PIPE_WIDTH:
                    self.pipes.pop(0)
                    self.pipes.append(self.create_pipe())
                    
                # Check for collisions
                self.handle_collision()
            
            # Drawing
            self.screen.blit(self.bg_img, (0, 0))
            self.draw_pipes()
            self.draw_bird()
            self.draw_score()
            
            if self.game_over:
                self.draw_game_over()
            
            pygame.display.update()
            self.clock.tick(60)
            
        pygame.quit()

if __name__ == "__main__":
    game = FlappyBird()
    game.run()