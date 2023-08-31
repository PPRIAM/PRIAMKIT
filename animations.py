import pygame, os, utils

class AnimationManager:
    def __init__(self, name, base_path="data/entities") -> None:
        self.current_state = "idle"
        self.animations = self.load_animations(base_path, name)

    def load_animations(self, base_path, name):
        return {animations:Animation(animations, base_path+name+'/animations/') for animations in os.listdir(base_path+name+'/animations')}

    def update(self):
        try:
            self.animations[self.current_state].play()
        except KeyError:
            print("This state is not available. There's the available states.:", self.get_states())

    def get_frame(self, flip):
        try:
            return self.animations[self.current_state].get_frame(flip)
        except KeyError:
            print("This state is not available. There's the available states.:", self.get_states())
    
    def get_states(self):
        return list(self.animations.keys())
    
    def set_state(self, state):
        self.current_state = state

class Animation:
    def __init__(self, animation_name, base_path) -> None:
        self.frames = self.load_frames(base_path, animation_name)
        self.current_frame = 0
        try:
            self.config = utils.load_json(base_path+'/'+animation_name+'/config.json')
        except:
            self.config = {
                "animation_speed":0.25,
                "loop": True,
                "done": False
            }
            utils.write_json(base_path+'/'+animation_name+'/config.json', self.config)

    def load_frames(self, base_path, animation_name):
        return [pygame.image.load(base_path+'/'+animation_name+'/'+image) for image in os.listdir(base_path+animation_name) if image.endswith('.png')]
    
    def play(self):
        if self.config["loop"]:
            self.current_frame += self.config["animation_speed"]
            if int(self.current_frame) > len(self.frames)-1:
                self.current_frame = 0
        else:
            if not self.config["done"]:
                self.current_frame += self.config["animation_speed"]
                if self.current_frame > len(self.frames):
                    self.config["done"] = True

    def get_frame(self, flip=False):
        if not flip:
            return self.frames[int(self.current_frame)-1]
        else:
            return pygame.tansform.flip(self.frames[int(self.current)], flip, False)
