import utils, math, pygame

class Gun:
    def __init__(self, holder, name, bullet_name, base_path="data/gun"):
        self.holder = holder
        self.name = name
        self.image = utils.load_image(base_path+'/'+self.name+'/'+self.name+'.png')
        self.image.set_colorkey((0, 0, 0))
        self.angle = 0
        self.rect = self.image.get_rect(center=self.holder.rect.center)
        self.bullet = bullet_name
        self.bullets = [] # [[Orgin pos], [pos], [speed], angle, offset]
        self.flip = False
        try:
            self.config = utils.load_json(base_path + "/"+self.name+"/"+"config.json")
        except:
            self.config = {
                "fire_rate":100,
                "magazine_capacity":15,
                "range":300,
                "type":"automatic",
            }
            utils.write_json(base_path + "/"+self.name+"/"+"config.json", self.config)
        self.magazine = self.config['magazine_capacity']
        self.amno = 0
        self.last_shoot = 0

    def get_angle(self, target:list):
        return math.atan2(target[1]-self.rect.centery, target[0]-self.rect.centerx)
    
    def update(self, target:pygame.rect.Rect):
        self.angle = self.get_angle(target)

        self.rect.centerx = self.holder.rect.centerx + (self.holder.rect.width//2+self.rect.width//2)*math.cos(self.angle)
        self.rect.centery = self.holder.rect.centery + (self.holder.rect.height//2+self.rect.height//2)*math.sin(self.angle) 
    
    def render(self, display):
        angle = self.angle
        if angle > math.pi/2 or angle < -math.pi/2:
            self.flip = True
            angle = -angle
        else:
            self.flip = False
        display.blit(pygame.transform.flip(pygame.transform.rotate(self.image, math.degrees(-angle)), False, self.flip), self.rect)

    def add_bullets(self, target, offset=0):
        if pygame.time.get_ticks()-self.last_shoot > self.config['fire_rate']:
            if self.magazine > 0:
                self.bullets.append(Bullet(self.bullet, [self.rect.centerx+self.rect.width/2*math.cos(self.angle), self.rect.centery+self.rect.height/2*math.sin(self.angle)], self.angle))
                self.magazine -= 1
                self.last_shoot = pygame.time.get_ticks()

    def set_amno(self, amno):
        self.amno = amno

    def reload(self):
        if self.magazine < self.config['magazine_capacity'] and self.holder.inventory.inventory[self.bullet] > 0:
            bulletToReload = min(self.config['magazine_capacity']-self.magazine, self.holder.inventory.inventory[self.bullet])
            print(bulletToReload)
            self.magazine += bulletToReload
            self.holder.inventory.inventory[self.bullet] -= bulletToReload

    def shoot(self, display, current_time):
        for bullet in self.bullets:
            bullet.render(display)
            bullet.update()

            if bullet.isTooFar(self.config['range']):
                self.bullets.remove(bullet)
        
class Bullet:
    def __init__(self, name, origin, angle, base_path="data/bullet") -> None:
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
        self.origin = origin
        self.rect = self.image.get_rect(center=origin)
        self.angle = angle

    def update(self):
        self.rect.centerx += self.config['speed']*math.cos(self.angle)
        self.rect.centery += self.config['speed']*math.sin(self.angle)

    def render(self, display):
        display.blit(pygame.transform.rotate(self.image, math.degrees(-self.angle)), self.rect)

    def isTooFar(self, distance):
        return utils.magnitude(self.rect, pygame.rect.Rect(self.origin[0], self.origin[1], 1, 1)) > distance
