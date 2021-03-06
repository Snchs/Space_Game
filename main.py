import pygame
import random

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 672, 608
FPS = 15

ENEMY_EVENT_TYPE = 30




# класс главного героя
class Hero(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 12)

# класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position
        self.direction = direction


    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        if self.direction == -1:
            pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 5)
        else:
            pygame.draw.circle(screen, (255, 0, 255), (self.x, self.y), 5)
# класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position
        self.direction = 1
        self.kd = 0

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 12)

# класс игры
class Game:
    def __init__(self, hero):
        self.hero = hero
        self.bullets = []
        self.enemies = []
        self.enemies_coords = []

    # отрисовка всех динамичных объектов
    def render(self, screen):
        self.hero.render(screen)
        for enemy in self.enemies:
            enemy.render(screen)

        for bullet in self.bullets:
            bullet.render(screen)

    # движение главного героя
    def move_hero(self):

        next_x, next_y = self.hero.get_position()

        if pygame.key.get_pressed()[pygame.K_a]:
            next_x -= 10
        if pygame.key.get_pressed()[pygame.K_d]:
            next_x += 10
        if pygame.key.get_pressed()[pygame.K_w]:
            next_y -= 10
        if pygame.key.get_pressed()[pygame.K_s]:
            next_y += 10
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.bullets.append(Bullet((next_x, next_y), -1))

        self.hero.set_position((next_x, next_y))

    # движение пули
    def move_bullets(self):

        # проход по всем действующим пулям
        for bullet in self.bullets:
            bullet.set_position((bullet.get_position()[0], bullet.get_position()[1] + bullet.direction * 15))

            # выход пули за пределы экрана
            if bullet.get_position()[1] < 0:
                del self.bullets[0]
            if bullet.get_position() in self.enemies_coords:
                # print("shot")
                for i, enemy in enumerate(self.enemies):
                    if enemy.get_position() == bullet.get_position():
                        del self.enemies[i]

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    # движение врагов
    def move_enemies(self):
        for i, enemy in enumerate(self.enemies):
            if enemy.get_position()[0] > WINDOW_WIDTH:
                enemy.direction = -1
            elif enemy.get_position()[0] < 0:
                enemy.direction = 1

            enemy.kd += 1

            if enemy.kd == 30:
                self.bullets.append(Bullet(enemy.get_position(), 1))
                enemy.kd = 0

            enemy.set_position((enemy.get_position()[0] + 10 * enemy.direction, enemy.get_position()[1]))
            if len(self.enemies_coords) > i:
                self.enemies_coords[i] = enemy.get_position()
            else:
                self.enemies_coords.append(enemy.get_position())


    # def move_enemy(self):
    #     next_position = self.labyrinth.find_path_step(self.enemy.get_position(), self.hero.get_position())
    #     self.enemy.set_position(next_position)
    #
    # def check_win(self):
    #     return self.labyrinth.get_tile_id(self.hero.get_position()) == self.labyrinth.finish_tile

    # def check_lose(self):
    #     return self.hero.get_position() == self.enemy.get_position()
#

# def show_message(screen, message):
#     font = pygame.font.Font(None, 50)
#     text = font.render(message, True, (50, 70, 0))
#     text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
#     text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
#     text_w = text.get_width()
#     text_h = text.get_height()
#     pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
#     screen.blit(text, (text_x, text_y))




def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    # all_sprites = pygame.sprite.Group()
    hero = Hero((150, 159))

    game = Game(hero)

    # all_sprites.add(labyrinth)
    # all_sprites.add(hero)
    # all_sprites.add(enemy)


    clock = pygame.time.Clock()
    counter = 0

    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_EVENT_TYPE and not game_over:
                 # game.move_enemy()
                 pass
                 # hero.render(screen)

        if game_over is False:

            game.move_hero()
            game.move_bullets()
            game.move_enemies()
            # print(counter)
            if counter % 100 ==0:
                counter = 0
                enemy = Enemy((random.randint(0, 600), random.randint(0, 250)))
                game.add_enemy(enemy)


        # Обновление
        #all_sprites.update()
        # for sprite in all_sprites:
        #     sprite.x -= 5
        screen.fill((0, 0, 0))
        game.render(screen)
        # if game.check_win():
        #     game_over = True
        #     show_message(screen, "YOU WON!")
        # elif game.check_lose():
        #     game_over = True
        #     show_message(screen, "YOU LOST!")

        pygame.display.flip()
        clock.tick(FPS)
        counter += 1
    pygame.quit()


if __name__ == "__main__":
    main()
