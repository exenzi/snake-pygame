import time
import pygame
from pygame import Surface
from pygame.locals import *
from snake import Snake
from settings import *

snake = Snake(ROWS, COLUMNS, UNLIMITED)

# Инициализация pygame
pygame.init()
pygame.font.init()

# Создание экрана
res_x = COLUMNS * CELL_WIDTH + CELL_BORDER * (COLUMNS - 1) + OFFSET * 2
res_y = ROWS * CELL_WIDTH + CELL_BORDER * (ROWS - 1) + OFFSET * 2
screen = pygame.display.set_mode((res_x, res_y))

# Иконка и название окна
pygame.display.set_caption('Змейка')
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)
# myfont = pygame.font.SysFont('Arial', FONT_SIZE)
myfont = pygame.font.Font('OpenSans-Regular.ttf', FONT_SIZE)

start = time.time()
direction = None
running = True
paused = False

paused_text = myfont.render(PAUSE_TEXT, ANTIALIAZING, TEXT_COLOR)
paused_text_position = (res_x // 2 - myfont.size(PAUSE_TEXT)[0] // 2,
                        res_y // 2 - myfont.size(PAUSE_TEXT)[1] // 2)

endgame_text = myfont.render(ENDGAME_TEXT, ANTIALIAZING, TEXT_COLOR)
endgame_text_position = (res_x // 2 - myfont.size(ENDGAME_TEXT)[0] // 2,
                         res_y // 2 - myfont.size(ENDGAME_TEXT)[1] // 2)

score_text = myfont.render(
    f'{SCORE_TEXT} 0', ANTIALIAZING, TEXT_COLOR)

how_pause_text = myfont.render(
    HOW_PAUSE_TEXT, ANTIALIAZING, TEXT_COLOR
)
how_pause_text_position = (
    10, res_y - myfont.size(ENDGAME_TEXT)[1] - myfont.size(QUIT_TEXT)[1] - 20)

quit_text = myfont.render(
    QUIT_TEXT, ANTIALIAZING, TEXT_COLOR
)
quit_text_position = (10, res_y - myfont.size(QUIT_TEXT)[1] - 10)

gray_bg = Surface((res_x, res_y), pygame.SRCALPHA)
gray_bg.fill(Color(0, 0, 0, 150))


while running:

    screen.fill(BORDER_COLOR)

    # Проверить закрытие игры
    if not snake.finish() and not paused:
        if time.time() - start > DELAY:
            snake.tick(direction)
            score_text = myfont.render(
                f'{SCORE_TEXT} {snake.score()}', ANTIALIAZING, TEXT_COLOR)
            start = time.time()

    rows = snake.get_board()
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            cell_color = ''
            if snake.is_head(y, x):
                cell_color = HEAD_COLOR
            elif cell == 0:
                cell_color = BG_COLOR
            elif cell == 1:
                cell_color = SNAKE_COLOR
            elif cell == 2:
                cell_color = SNACK_COLOR
            pygame.draw.rect(screen, cell_color,
                            Rect(OFFSET + CELL_BORDER*x + x*CELL_WIDTH,
                                OFFSET + CELL_BORDER*y + y*CELL_WIDTH,
                                CELL_WIDTH, CELL_WIDTH))

    
    if paused:
        screen.blit(gray_bg, (0, 0))
        screen.blit(paused_text, paused_text_position)

    if snake.finish():
        screen.blit(gray_bg, (0, 0))
        screen.blit(endgame_text, endgame_text_position)

    screen.blit(score_text, (10, 10))
    screen.blit(how_pause_text, how_pause_text_position)
    screen.blit(quit_text, quit_text_position)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print('Финальный счёт:', snake.score())
        
        if event.type == pygame.KEYDOWN:
            print('Нажата клавиша:', pygame.key.name(event.key))
            
            if event.key == pygame.K_q:
                running = False
                print('Финальный счёт:', snake.score())

            if not snake.finish():
                if event.key == pygame.K_UP:
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                elif event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                elif event.key == pygame.K_SPACE:
                    if paused:
                        paused = False
                        print('Пауза: отключить')
                    else:
                        paused = True
                        print('Пауза: включить')
            else:
                snake = Snake(ROWS, COLUMNS, UNLIMITED)
                paused = False

    
    pygame.display.update()




