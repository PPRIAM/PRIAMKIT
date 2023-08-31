import utils, math, pygame

class Gun:
    def __init__(self, holder:pygame.rect.Rect, name, bullet, base_path="data/gun"):
        self.holder = holder
        self.name = name
        self.image = utils.load_image(base_path+'/'+self.name+'/'+self.name+'.png')
        self.image.set_colorkey((0, 0, 0))
        self.angle = 0
        self.rect = self.image.get_rect(center=self.holder.center)
        self.bullet = bullet
        self.bullets = [] # [[Orgin pos], [pos], [speed], angle, offset]
        try:
            self.config = utils.load_json(base_path + "/"+self.name+"/"+"config.json")
        except:
            self.config = {
                "fire_rate":100,
                "magazine_capacity":100,
                "range":300,
                "type":"automatic",
            }
            utils.write_json(base_path + "/"+self.name+"/"+"config.json", self.config)
        self.magazine = self.config['magazine_capacity']
        self.amno = 0

    def get_angle(self, target:list):
        return math.atan2(target[1]-self.rect.centery, target[0]-self.rect.centerx)
    
    def update(self, target:pygame.rect.Rect):
        self.angle = self.get_angle(target)

        self.rect.centerx = self.holder.centerx + (self.holder.width//2+self.rect.width//2)*math.cos(self.angle)
        self.rect.centery = self.holder.centery + (self.holder.height//2+self.rect.height//2)*math.sin(self.angle) 
    
    def render(self, display):
        display.blit(pygame.transform.rotate(self.image, math.degrees(-self.angle)), self.rect)

    def add_bullets(self, offset=0):
        # [[Orgin pos], [pos], [speed], angle, offset]
        # [     0,        1,      2,      3,      4]
        if self.magazine > 0:
            self.bullets.append([[self.rect.centerx+self.rect.width//2*math.cos(self.angle), self.rect.centery+self.rect.height//2*math.sin(self.angle)], [self.rect.centerx+self.rect.width//2*math.cos(self.angle), self.rect.centery+self.rect.height//2*math.sin(self.angle)], self.bullet.config['speed'], self.angle, offset])
            self.magazine -= 1

    def set_amno(self, amno):
        self.amno = amno

    def reload(self):
        if self.magazine < self.config['magazine_capacity'] and self.amno > 0:
            bulletToReload = min(self.config['magazine_capacity']-self.magazine, self.amno)
            reloadedBullets = self.amno - bulletToReload
            self.magazine += reloadedBullets

    def shoot(self, display):
        last_shoot = pygame.time.get_ticks()
        for bullet in self.bullets:
            # Move the Bullets
            if pygame.time.get_ticks()-last_shoot > self.config['fire_rate']:
                last_shoot = pygame.time.get_ticks()
                bullet[1][0] += bullet[2]*math.cos(bullet[3])
                bullet[1][1] += bullet[2]*math.sin(bullet[3])-bullet[4]

            # Display the bullets
                display.blit(pygame.transform.rotate(self.bullet.image, math.degrees(-bullet[3])), bullet[1])

            # Remove the bullets
                if utils.magnitude(pygame.rect.Rect(bullet[0][0], bullet[0][1], 1, 1), pygame.rect.Rect(bullet[1][0], bullet[1][1], 1, 1)) > self.config['range']:
                    self.bullets.remove(bullet)
            


class Bullet:
    def __init__(self, name, base_path="data/bullet") -> None:
        self.name = name
        self.image = utils.load_image(base_path+'/'+self.name+'/bullet.png')
        self.image.set_colorkey((0, 0, 0))
        try:
            self.config = utils.load_json(base_path+'/'+self.name+'/config.json')
        except:
            self.config = {
                "damage": 1,
                "speed": 10,
            }
            utils.write_json(base_path+'/'+self.name+'/config.json', self.config)
