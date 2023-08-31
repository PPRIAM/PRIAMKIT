import pygame, sys, time, entities, weapon, random

pygame.init()

class Game:
    def __init__(self, title='Untitled', screen_size=[640, 480], fps=60):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.startTime = time.time()
        self.startTick = pygame.time.get_ticks()

        self.display = pygame.Surface([320, 240])

        # Shiro
        self.shiro = entities.Entity("Player", position=[self.display.get_width()//2, self.display.get_height()//2])

        self.mps5 = weapon.Gun(self.shiro.rect, "mps5", weapon.Bullet("normal"))
        self.normalBullet = weapon.Bullet("normal")

        self.mouse = {button:False for button in ["left","middle","right"]}

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.clock.tick(self.fps)

            self.display.fill((0, 0, 0))

            self.shiro.render(self.display)
            self.shiro.update()

            self.mps5.update([pygame.mouse.get_pos()[0]//2, pygame.mouse.get_pos()[1]//2])
            self.mps5.render(self.display)
            #print(self.mps5.bullets)

            if self.mps5.config['type'] == 'automatic':
                if self.mouse['left']:
                    self.mps5.shoot(self.display)
            self.mps5.add_bullets(random.randint(-1, 1))
            self.mps5.set_amno(1000)
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), (0, 0))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a: self.shiro.movement[0] -= 1
                    if event.key == pygame.K_d: self.shiro.movement[0] += 1
                    if event.key == pygame.K_w: self.shiro.movement[1] -= 1
                    if event.key == pygame.K_s: self.shiro.movement[1] += 1
                    if event.key == pygame.K_r: self.mps5.reload()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a: self.shiro.movement[0] += 1
                    if event.key == pygame.K_d: self.shiro.movement[0] -= 1
                    if event.key == pygame.K_w: self.shiro.movement[1] += 1
                    if event.key == pygame.K_s: self.shiro.movement[1] -= 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse['left'] = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse['left'] = False
                
Game("Gaem").run()
