import pygame, sys, time, entities

pygame.init()

class Game:
    def __init__(self, title='Untitled', screen_size=[640, 480], fps=60):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.startTime = time.time()

        self.display = pygame.Surface([320, 240])

        # Shiro
        self.shiro = entities.Entity("Player", position=[50, 50])

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.clock.tick(self.fps)
            dt = 1

            self.display.fill((0, 0, 0))

            self.shiro.render(self.display)
            self.shiro.update()

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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a: self.shiro.movement[0] += 1
                    if event.key == pygame.K_d: self.shiro.movement[0] -= 1
                    if event.key == pygame.K_w: self.shiro.movement[1] += 1
                    if event.key == pygame.K_s: self.shiro.movement[1] -= 1

title = input("Enter the game title:")
Game(title).run()
