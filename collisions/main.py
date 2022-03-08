import pygame
import numpy as np

pygame.init()
WIDTH = 600
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collisions")
clock = pygame.time.Clock()


class Ball(pygame.sprite.Sprite):
    radius = 5
    vel = np.array([0, 0])

    def __init__(self, x, y, id):
        super().__init__()

        self.pos = np.array([x, y])
        self.id = id

        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(self.image, (23, 12, 43), (x, y), self.radius)
        self.rect = self.image.get_rect(center=(x + self.radius, y + self.radius))

    def update(self):
        self.vel += np.array([0, 1])
        self.move()

    def move(self):
        self.pos += self.vel
        self.rect.center = (self.pos[0], self.pos[1])


def main():
    run = True
    ball_group = pygame.sprite.Group()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse has been lcicked")
                x, y = pygame.mouse.get_pos()
                ball = Ball(x, y, 1)
                ball_group.add(ball)

        SCREEN.fill((255, 255, 255))

        ball_group.draw(SCREEN)
        ball_group.update()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

