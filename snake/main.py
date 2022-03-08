import pygame

pygame.init()
width = 700
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Snake:
    def __init__(
        self, key_binds, boundary, color=(255, 255, 255), startVelocity=[0, -1]
    ):
        if len(key_binds) < 4:
            raise "Not enough keybinds"
        self.key_binds = {
            "up": key_binds[0],
            "down": key_binds[1],
            "left": key_binds[2],
            "right": key_binds[3],
        }

        self.boundary = boundary
        self.color = color
        self.vel = startVelocity
        self.boxes = [[boundary[0] // 2, boundary[1] // 2]]
        self.alive = True

    def update(self, keys_pressed):
        if keys_pressed[self.key_binds["up"]]:
            self.vel = [0, -1]
        elif keys_pressed[self.key_binds["down"]]:
            self.vel = [0, 1]
        elif keys_pressed[self.key_binds["left"]]:
            self.vel = [-1, 0]
        elif keys_pressed[self.key_binds["right"]]:
            self.vel = [1, 0]

        self.move()

    def move(self):
        newBox = [self.boxes[0][0] + self.vel[0], self.boxes[0][1] + self.vel[1]]
        self.boxes = [newBox] + self.boxes


def main():
    run = True

    snake = Snake(
        [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d],
        [width / 10, height / 10],
        None,
    )

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

        screen.fill(WHITE)
        pygame.display.flip()
        snake.update(pygame.key.get_pressed())
        snake.
        clock.tick(15)


if __name__ == "__main__":
    main()

