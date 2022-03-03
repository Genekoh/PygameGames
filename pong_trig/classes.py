import pygame
import numpy as np

WHITE = (255, 255, 255)


class Paddle(pygame.sprite.Sprite):
    velocity = 8

    def __init__(
        self,
        pos,
        width,
        height,
        up_key,
        down_key,
        min_y,
        max_y,
        color=WHITE,
    ):
        super().__init__()

        x, y = pos
        self.start_pos = np.array([x, y])
        self.pos = np.array([x, y])
        self.width = width
        self.height = height
        self.up_key = up_key
        self.down_key = down_key

        self.min_y = min_y
        self.max_y = max_y

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x + width / 2, y + height / 2))

    def update(self, keys):
        if keys[self.up_key]:
            self.move(True)
        elif keys[self.down_key]:
            self.move(False)

    def move(self, up):
        if up:
            new_pos = self.pos + np.array([0, -self.velocity])
            if new_pos[1] < self.min_y:
                new_pos[1] = self.min_y

            self.pos = new_pos
            self.rect.center = (
                new_pos[0] + self.width / 2,
                new_pos[1] + self.height / 2,
            )
        else:
            new_pos = self.pos + np.array([0, self.velocity])
            if new_pos[1] + self.height > self.max_y:
                new_pos[1] = self.max_y - self.height

            self.pos = new_pos
            self.rect.center = (
                new_pos[0] + self.width / 2,
                new_pos[1] + self.height / 2,
            )

    def reset(self):
        self.pos = self.start_pos


class Ball(pygame.sprite.Sprite):
    MAX_SPEED = 15
    START_SPEED = 5

    def __init__(self, pos, size, color=WHITE):
        super().__init__()

        x, y = pos
        self.size = size
        self.start_pos = np.array([x, y])
        self.pos = np.array([x, y])
        self.reset_direction = np.random.choice([True, False])
        self.vel = self.randomDirection(self.START_SPEED, self.reset_direction)

        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)

    def randomDirection(self, velocity, right=True):
        # Range of -pi/4 to pi/4
        max = np.pi / 4
        min = -np.pi / 4
        theta = (max - min) * np.random.random() + min
        vx = velocity * np.cos(theta)
        vy = velocity * np.sin(theta)

        if not right:
            vx = -vx

        return np.array([vx, vy])

    def update(self):
        self.pos += self.vel
        self.rect.center = (self.pos[0], self.pos[1])

    def accelerate(self, speedInc):
        new_speed = np.linalg.norm(self.vel) + speedInc
        if new_speed > self.MAX_SPEED:
            new_speed = self.MAX_SPEED

        new_vel = self.vel / np.linalg.norm(self.vel) * new_speed
        self.vel = new_vel

    def collide_x(self):
        x_vel, y_vel = self.vel[0], self.vel[1]
        if y_vel > 0:
            self.vel = np.array([x_vel, -np.abs(y_vel)])
        else:
            self.vel = np.array([x_vel, np.abs(y_vel)])
            

    def collide_paddle(self, displacement):
        # angel ranges from pi/4 to -pi/4
        # displacement is 1 : theta = pi/4
        # displacement is 0 : theta = 0
        # displacement is -1 : theta = -pi/4

        print("displacement", displacement)
        cur_speed = np.linalg.norm(self.vel)
        max = np.pi / 4
        min = 0
        theta = (max - min) * (-displacement) + min

        vx = cur_speed * np.cos(theta) * (-self.vel[0] / np.abs(self.vel[0]))
        vy = cur_speed * np.sin(theta)
        self.vel = np.array([vx, vy])

        self.accelerate((self.MAX_SPEED - self.START_SPEED) / 3)

    def reset(self):
        start_x = self.start_pos[0]
        start_y = self.start_pos[1]
        self.pos = np.array([start_x, start_y])
        self.reset_direction = not self.reset_direction
        self.vel = self.randomDirection(self.START_SPEED, self.reset_direction)
