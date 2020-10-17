import random


class Snake:

    def __init__(self, rows, columns, unlimited = False):
        self.rows = rows
        self.columns = columns
        self.snake = [(rows // 2 - 1, columns // 2 - 1)]
        self.direction = 'right'
        self.snacks = set()
        self.add_snack()
        self.current_score = 0
        self.finished = False
        self.unlimited = unlimited
        print('Змейка инициализирована')

    def tick(self, direction=None):
        print(self.snake)
        if direction:
            if (self.direction == 'up' and direction != 'down') or \
                    (self.direction == 'down' and direction != 'up') or \
                    (self.direction == 'left' and direction != 'right') or \
                    (self.direction == 'right' and direction != 'left'):
                self.direction = direction
        new_cell = None
        if self.direction == 'right':
            new_cell = (self.snake[0][0], self.snake[0][1] + 1)
        elif self.direction == 'left':
            new_cell = (self.snake[0][0], self.snake[0][1] - 1)
        elif self.direction == 'up':
            new_cell = (self.snake[0][0] - 1, self.snake[0][1])
        elif self.direction == 'down':
            new_cell = (self.snake[0][0] + 1, self.snake[0][1])
        if not self.finish(new_cell):
            self.snake.insert(0, new_cell)
            # Проверть не съедена ли еда
            if self.snake[0] in self.snacks:
                self.snacks.discard(self.snake[0])
                self.add_snack()
                self.current_score += 1
            else:
                del self.snake[-1]
        else:
            self.finished = True


    def get_board(self):
        # Создаём поле
        board = []
        for row in range(self.rows):
            new_row = []
            for column in range(self.columns):
                if (row, column) in self.snake:
                    new_row.append(1)
                elif (row, column) in self.snacks:
                    new_row.append(2)
                else:
                    new_row.append(0)
            board.append(new_row)
        return board

    def is_head(self, y, x):
        if self.snake[0] == (y, x):
            return True
        return False

    def add_snack(self):
        while True:
            new_snack = (random.randrange(0, self.rows - 1),
                         random.randrange(0, self.columns - 1))

            # Проверка на расположение еды внутри змейки/ другой еды
            if new_snack not in self.snake and new_snack not in self.snacks:
                break
        self.snacks.add(new_snack)

    def score(self):
        return self.current_score

    def finish(self, *cell):
        if self.finished:
            return True

        if cell:
            new_head = cell[0]
        else:
            new_head = self.snake[0]

        if new_head in self.snake[1:] or new_head[0] < 0 or new_head[0] > self.rows - 1 \
                or new_head[1] < 0 or new_head[1] > self.columns - 1:
            return True
        else:
            return False
