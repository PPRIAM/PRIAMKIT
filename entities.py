from animations import AnimationManager

class Entity:
    def __init__(self, name:str=None, position=[0, 0], velocity=[1, 1]) -> None:
        self.animations = AnimationManager(name, base_path="data/entity/")
        self.flip = False
        self.image = self.animations.get_frame(self.flip).convert()
        self.rect = self.image.get_rect(center=position)
        self.movement = [0, 0]
        self.velocity = velocity

    def render(self, display):
        try:
            display.blit(self.image, self.rect)
        except TypeError:
            print("Can't render")

    def update(self):
        if self.movement[0] == 0 and self.movement[1] == 0:
            self.animations.set_state("idle")
        self.animations.update()
        self.image = self.animations.get_frame(self.flip).convert()
        if self.movement[0] != 0 or self.movement[1] != 0:
            self.animations.set_state("run")
        self.move()

    def move(self):
        self.rect.x += self.velocity[0]*self.movement[0]
        self.rect.y += self.velocity[1]*self.movement[1]
        