import json, pygame, math

def load_json(path):
    with open(path, 'r') as f:
        content = json.loads(f.read())
    return content

def write_json(path, content, indent=4):
    with open(path, 'w') as f:
        f.write(json.dumps(content, indent=indent))

def clamp(value, min1, max1, min2, max2):
    return min2 + (max2-min2)*((value-min1)/(max1-min1))

def load_image(path:str) -> pygame.Surface:
    return pygame.image.load(path).convert()

def magnitude(rect1:pygame.rect.Rect, rect2:pygame.rect.Rect) -> float:
    return math.sqrt((rect1.centerx-rect2.centerx)**2+(rect1.centery-rect2.centery)**2)