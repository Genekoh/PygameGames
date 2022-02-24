import pygame
from classes import Paddle, Ball

pygame.init()
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()


def main():
    run = True

    paddle_width = 10
    paddle_height = 60

    left_paddle = Paddle(
        (10, SCREEN_HEIGHT / 2 - paddle_height / 2),
        paddle_width,
        paddle_height,
        pygame.K_w,
        pygame.K_s,
        10,
        SCREEN_HEIGHT - 10,
    )

    right_paddle = Paddle(
        (SCREEN_WIDTH - paddle_width - 10, SCREEN_HEIGHT / 2 - paddle_height / 2),
        paddle_width,
        paddle_height,
        pygame.K_UP,
        pygame.K_DOWN,
        10,
        SCREEN_HEIGHT - 10,
    )
    paddles = pygame.sprite.Group()
    paddles.add(left_paddle, right_paddle)

    ball = Ball((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 15)
    balls_group = pygame.sprite.Group()
    balls_group.add(ball)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

        WINDOW.fill((25, 25, 25))
        paddles.draw(WINDOW)
        paddles.update(pygame.key.get_pressed())

        balls_group.draw(WINDOW)
        balls_group.update()
        handle_collision(ball, left_paddle, right_paddle)

        pygame.display.flip()
        clock.tick(60)


def handle_collision(ball, left_paddle, right_paddle):
    ball_x = ball.pos[0]
    ball_y = ball.pos[1]

    if ball_y <= 0 or ball_y + ball.size >= SCREEN_HEIGHT:
        print("colliding with x axis")
        ball.collide_x()
    elif (
        ball_x <= left_paddle.pos[0] + left_paddle.width
        and ball_y > left_paddle.pos[1]
        and ball_y < left_paddle.pos[1] + left_paddle.height
    ):
        ball_center = ball_y + ball.size / 2
        left_paddle_center = left_paddle.pos[1] + left_paddle.height / 2
        displacement = left_paddle_center - ball_center
        ball.collide_paddle(displacement / (left_paddle.height / 2))
        print("colliding with left paddle")
    elif (
        ball_x + ball.size >= right_paddle.pos[0]
        and ball_y > right_paddle.pos[1]
        and ball_y < right_paddle.pos[1] + right_paddle.height
    ):
        ball_center = ball_y + ball.size / 2
        right_paddle_center = right_paddle.pos[1] + right_paddle.height / 2
        displacement = right_paddle_center - ball_center
        ball.collide_paddle(displacement / (right_paddle.height / 2))
        print("colliding with right paddle")
    else:
        check_win(ball)


def check_win(ball):
    if ball.pos[0] <= -50:
        ball.reset()
    if ball.pos[0] + ball.size >= SCREEN_WIDTH + 50:
        ball.reset()


if __name__ == "__main__":
    main()
