import pygame
import time
from game.components.spaceship import Spaceship
from game.utils.constants import  BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, DEFAULT_TYPE
from game.components.enemies.enemy_manager import EnemyManager
from game.components.bullets.bullet_manager import BulletManager
from game.components.menu import Menu
from game.components.power_ups.power_up_manager import PowerUpManager

class Game:
    HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
    HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2

    def __init__(self):
        self.scores = []
        self.best_score = 0
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.playing = False
        self.game_speed = 10
        
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Spaceship()
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        self.running = False
        self.score = 0
        self.death_count = 0
        self.menu = Menu('Press any key to start...', self.HALF_SCREEN_WIDTH, self.HALF_SCREEN_HEIGHT, self.screen)
        self.power_up_manager = PowerUpManager()
        
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()
    
    def reset(self):
        self.power_up_manager.reset()

    def run(self):
        self.enemy_manager.reset()
        self.score = 0
        
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
    
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self)
        self.enemy_manager.update(self)
        self.bullet_manager.update(self)
        self.power_up_manager.update(self)
    
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255,255,255))
        
        self.draw_background()
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.draw_score()
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        pygame.display.update()
        pygame.display.flip()

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.menu.draw(self.screen, f'{self.player.power_up_type.capitalize()} is enabled for {time_to_show} in seconds', 500, 50, (255,255,255))
            else:
                self.player.has_power_up = False
                self.player.power_time_up = DEFAULT_TYPE
                self.player.set_image()
        
    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg = self.y_pos_bg + self.game_speed
        
    def show_menu(self):
        self.menu.reset_screen_color(self.screen)
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        
        if self.death_count == 0:
            self.menu.draw(self.screen)
        else:
            self.menu.update_message("Game over.", self.HALF_SCREEN_WIDTH, self.HALF_SCREEN_HEIGHT)
            self.menu.draw(self.screen)
            self.menu.update_message(f'Your score: {self.score}', self.HALF_SCREEN_WIDTH, self.HALF_SCREEN_HEIGHT + 50)
            self.menu.draw(self.screen)
            self.menu.update_message(f'Highest score: {self.best_score}', self.HALF_SCREEN_WIDTH, self.HALF_SCREEN_HEIGHT + 100)
            self.menu.draw(self.screen)
            self.menu.update_message(f'Total deaths: {self.death_count}', self.HALF_SCREEN_WIDTH, self.HALF_SCREEN_HEIGHT + 150)
            self.menu.draw(self.screen)
            
        icon = pygame.transform.scale(ICON, (80,120))
        self.screen.blit(icon, (half_screen_width - 50, half_screen_height -150))
        self.menu.update(self)
        
    def update_score(self):
        self.score +=1
        self.scores.append(self.score)
        self.best_score = max(self.scores)
        
    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score}', True, (255,255,255)) 
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH - 100, 50) 
        self.screen.blit(text, text_rect)   