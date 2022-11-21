import pygame
import random
import sys
import pygame_menu
pygame.init()

bg_image = pygame.image.load("pop.jpg")
SIZE_BLOCK = 20
FRAME_WORK = (0, 255, 204)
BLUE = (204, 255, 255)
WHITE = (255, 255, 255)
RED = (224, 0, 0)
STONE_COLOR = (128, 128, 128)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
BAD_SNAKE_COLOR = (17, 0, 51)
COUNT_BLOCKS = 20
COUNT_LINES = 30
MARGIN = 1
HEADER_MARGIN = 70
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * SIZE_BLOCK,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * SIZE_BLOCK + HEADER_MARGIN]
print(size)
screen = pygame.display.set_mode(size)  # create a window
pygame.display.set_caption("Snake")  # title
timer = pygame.time.Clock()  # time
courier = pygame.font.SysFont('courier', 36)
arial = pygame.font.SysFont('arial', 36)
name = 'Player1'
difficulty_of_game = 1


def set_color(value, color):
    global SNAKE_COLOR
    if color == 1:
        SNAKE_COLOR = (0, 102, 0)
    elif color == 2:
        SNAKE_COLOR = (255, 255, 0)
    elif color == 3:
        SNAKE_COLOR = (179, 0, 179)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < SIZE_BLOCK and 0 <= self.y < SIZE_BLOCK
    # head in snake_blocks

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color_, column_, line_):
    # drawing the square
    pygame.draw.rect(screen, color_, [SIZE_BLOCK + column_ * SIZE_BLOCK + column_,
                                      HEADER_MARGIN + SIZE_BLOCK + line_ * SIZE_BLOCK + line_,
                                      SIZE_BLOCK, SIZE_BLOCK])


def my_text_value(name_="Player1"):
    global name
    name = name_


def set_difficulty(value, difficulty=1):
    global difficulty_of_game
    difficulty_of_game = difficulty


class Records:
    def __init__(self, file_of_records):
        self.file_of_records = file_of_records
        r_file_of_records = open(file_of_records, "r")
        self.all_players = r_file_of_records.readlines()
        self.all_to_read = '\n'.join(self.all_players)
        r_file_of_records.close()
        self.is_updated = False

    def of_the_player(self):
        of_the_player = 0
        if self.all_to_read.find('/' + name + '/') == -1:
            print('all_to_read', self.all_to_read)
            of_the_player = 0
            self.all_players.append(f'/{of_the_player}/{name}/\n')
        else:
            for lines in self.all_players:
                if lines.find('/' + name + '/') != -1:
                    of_the_player = int(lines.split('/')[1])
                    break
        return of_the_player

    def of_all_players(self):
        return self.all_players

    def update_of_the_player(self, total, total_record):
        tot_rec = total_record
        if total > tot_rec:
            self.is_updated = True
            tot_rec = total
        return tot_rec

    def update_list_all_players(self, total_record):
        def res_key(line_):
            list_line = line_.split('/')
            print(list_line)
            return int(list_line[1])

        if self.is_updated:
            lol_flag = 1
            for lines in range(len(self.all_players)):
                if self.all_players[lines].find(name) != -1 and lol_flag != -1:
                    self.all_players[lines] = f'/{total_record}/{name}/\n'
                    print('all_record_lines', self.all_players)
                    lol_flag = -1
            self.all_players.sort(reverse=True, key=res_key)
            w_file_of_records = open(self.file_of_records, "w")
            for lines in self.all_players:
                print(lines)
                w_file_of_records.write(lines)
            w_file_of_records.close()

    def print(self):
        pass


class SnakeLevels:

    @staticmethod
    def easy_play_level():

        global name

        def get_empty_random_block():
            x = random.randint(0, COUNT_BLOCKS - 1)
            y = random.randint(0, COUNT_BLOCKS - 1)
            empty_block = SnakeBlock(x, y)
            while empty_block in snake_blocks:
                empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
                empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
            return empty_block

        x0 = random.randint(0, COUNT_BLOCKS - 5)
        y0 = random.randint(0, COUNT_BLOCKS - 1)

        snake_blocks = [SnakeBlock(x0, y0), SnakeBlock(x0 + 1, y0), SnakeBlock(x0 + 2, y0)]  # a head is last
        apple = get_empty_random_block()
        stone = get_empty_random_block()
        d_line = 0
        d_col = 1
        speed = 0
        total = 0
        records = Records("records1.txt")
        total_record = records.of_the_player()
        while True:
            for event in pygame.event.get():  # doing all events
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and d_col != 0:
                        d_line = -1
                        d_col = 0
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and d_col != 0:
                        d_line = 1
                        d_col = 0
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and d_line != 0:
                        d_line = 0
                        d_col = -1
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and d_line != 0:
                        d_line = 0
                        d_col = 1

            screen.fill(FRAME_WORK)
            pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

            text_total = courier.render(f"Total: {total}", False, WHITE)
            text_record = courier.render(f"Record: {total_record}", False, WHITE)
            screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
            screen.blit(text_record, (SIZE_BLOCK + 210, SIZE_BLOCK))
            for line in range(COUNT_BLOCKS):
                for column in range(COUNT_BLOCKS):
                    if (line + column) % 2 == 0:
                        color = WHITE
                    else:
                        color = BLUE
                    draw_block(color, column, line)

            head = snake_blocks[-1]
            if not head.is_inside():
                break

            draw_block(RED, apple.x, apple.y)
            for block in snake_blocks:
                draw_block(SNAKE_COLOR, block.x, block.y)
            if apple == head:
                total += 1
                total_record = records.update_of_the_player(total, total_record)
                speed = total // 2
                snake_blocks.append(apple)
                apple = get_empty_random_block()
            new_head = SnakeBlock(head.x + d_col, head.y + d_line)
            if new_head in snake_blocks:
                break
            snake_blocks.append(new_head)
            snake_blocks.pop(0)

            pygame.display.flip()  # we apply everything that we have drawn on the screen
            timer.tick(4 + speed)

        records.update_list_all_players(total_record)

    @staticmethod
    def medium_play_level():
        global name

        def get_empty_random_block():
            x = random.randint(0, COUNT_BLOCKS - 1)
            y = random.randint(0, COUNT_BLOCKS - 1)
            empty_block = SnakeBlock(x, y)
            while (empty_block in snake_blocks) or (empty_block in stone_blocks):
                empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
                empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
            return empty_block

        x0 = random.randint(0, COUNT_BLOCKS - 5)
        y0 = random.randint(0, COUNT_BLOCKS - 1)

        snake_blocks = [SnakeBlock(x0, y0), SnakeBlock(x0 + 1, y0), SnakeBlock(x0 + 2, y0)]  # a head is last
        stone_blocks = []
        stone = get_empty_random_block()
        stone_blocks.append(stone)
        apple = get_empty_random_block()
        stone = get_empty_random_block()
        d_line = 0
        d_col = 1
        speed = 0
        total = 0
        records = Records("records2.txt")
        total_record = records.of_the_player()
        while True:
            for event in pygame.event.get():  # doing all events
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and d_col != 0:
                        d_line = -1
                        d_col = 0
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and d_col != 0:
                        d_line = 1
                        d_col = 0
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and d_line != 0:
                        d_line = 0
                        d_col = -1
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and d_line != 0:
                        d_line = 0
                        d_col = 1

            screen.fill(FRAME_WORK)
            pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

            text_total = courier.render(f"Total: {total}", False, WHITE)
            text_record = courier.render(f"Record: {total_record}", False, WHITE)
            screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
            screen.blit(text_record, (SIZE_BLOCK + 210, SIZE_BLOCK))
            for line in range(COUNT_BLOCKS):
                for column in range(COUNT_BLOCKS):
                    if (line + column) % 2 == 0:
                        color = WHITE
                    else:
                        color = BLUE
                    draw_block(color, column, line)

            head = snake_blocks[-1]
            if not head.is_inside():
                break

            draw_block(RED, apple.x, apple.y)
            for stones in stone_blocks:
                draw_block(STONE_COLOR, stones.x, stones.y)
            for block in snake_blocks:
                draw_block(SNAKE_COLOR, block.x, block.y)
            if apple == head:
                total += 1
                total_record = records.update_of_the_player(total, total_record)
                speed = total // 2
                snake_blocks.append(apple)
                apple = get_empty_random_block()
                stone = get_empty_random_block()
                stone_blocks.append(stone)
            if head in stone_blocks:
                break
            new_head = SnakeBlock(head.x + d_col, head.y + d_line)
            if new_head in snake_blocks:
                break
            snake_blocks.append(new_head)
            snake_blocks.pop(0)

            pygame.display.flip()  # we apply everything that we have drawn on the screen
            timer.tick(4 + speed)

        records.update_list_all_players(total_record)

    @staticmethod
    def hard_play_level():
        global name

        def get_empty_random_block():
            x = random.randint(0, COUNT_BLOCKS - 1)
            y = random.randint(0, COUNT_BLOCKS - 1)
            empty_block = SnakeBlock(x, y)
            while empty_block in snake_blocks:
                empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
                empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
            return empty_block

        def check_bad_new_block(x, y):
            flag = 1
            empty_copy = SnakeBlock(x, y)
            moves = [(-1, 0), (0, 1), (1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for delta in moves:
                empty_copy.x += delta[0]
                empty_copy.y += delta[1]
                if not empty_copy.is_inside():
                    flag = 0
                empty_copy.x -= delta[0]
                empty_copy.y -= delta[1]
            if empty_copy in snake_blocks:
                flag = 0
            return flag

        def head_empty_random_block(head_x, head_y):
            move = [(-1, 0), (-1, 0), (0, 1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1),
                    (-1, 0), (-1, 0), (0, 1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1)]
            dx, dy = random.choice(move)
            x, y = dx + head_x, dy + head_y
            while not check_bad_new_block(x, y):
                dx, dy = random.choice(move)
                x, y = dx + head_x, dy + head_y
            empty_block = SnakeBlock(x, y)
            return empty_block

        x0 = random.randint(0, COUNT_BLOCKS - 5)
        y0 = random.randint(0, COUNT_BLOCKS - 1)

        snake_blocks = [SnakeBlock(x0, y0), SnakeBlock(x0 + 1, y0), SnakeBlock(x0 + 2, y0)]  # a head is last
        bad_snake_block = get_empty_random_block()
        bad_snake_blocks = [bad_snake_block]

        apple = get_empty_random_block()
        movement = dict(up=(-1, 0), down=(1, 0), left=(0, -1), right=(0, 1))
        d_line = 0
        d_col = 1
        speed = 0
        total = 0
        records = Records("records3.txt")
        total_record = records.of_the_player()
        while True:
            for event in pygame.event.get():  # doing all events
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and d_col != 0:
                        d_line, d_col = movement['up']
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and d_col != 0:
                        d_line, d_col = movement['down']
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and d_line != 0:
                        d_line, d_col = movement['left']
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and d_line != 0:
                        d_line, d_col = movement['right']

            screen.fill(FRAME_WORK)
            pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

            text_total = courier.render(f"Total: {total}", False, WHITE)
            text_record = courier.render(f"Record: {total_record}", False, WHITE)
            screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
            screen.blit(text_record, (SIZE_BLOCK + 210, SIZE_BLOCK))
            for line in range(COUNT_BLOCKS):
                for column in range(COUNT_BLOCKS):
                    if (line + column) % 2 == 0:
                        color = WHITE
                    else:
                        color = BLUE
                    draw_block(color, column, line)
            head_bad = bad_snake_blocks[-1]
            head = snake_blocks[-1]
            if not head.is_inside():
                break

            draw_block(RED, apple.x, apple.y)
            # for stones in stone_blocks:
            #     draw_block(STONE_COLOR, stones.x, stones.y)
            for block in snake_blocks:
                draw_block(SNAKE_COLOR, block.x, block.y)
            for block_bad in bad_snake_blocks:
                draw_block(BAD_SNAKE_COLOR, block_bad.x, block_bad.y)
            if apple == head:
                total += 1
                total_record = records.update_of_the_player(total, total_record)
                speed = total // 2
                snake_blocks.append(apple)
                bad_snake_blocks.append(head_bad)
                apple = get_empty_random_block()

            new_head = SnakeBlock(head.x + d_col, head.y + d_line)
            bad_new_head = head_empty_random_block(head_bad.x, head_bad.y)

            if (new_head in snake_blocks) or (new_head in bad_snake_blocks) or (head in bad_snake_blocks):
                break
            snake_blocks.append(new_head)
            bad_snake_blocks.append(bad_new_head)
            snake_blocks.pop(0)
            bad_snake_blocks.pop(0)

            pygame.display.flip()  # we apply everything that we have drawn on the screen
            timer.tick(4 + speed)

        records.update_list_all_players(total_record)


def start_the_game():
    global difficulty_of_game
    level = difficulty_of_game
    snake = SnakeLevels()
    if level == 1:
        snake.easy_play_level()
    elif level == 2:
        snake.medium_play_level()
    elif level == 3:
        snake.hard_play_level()

    # global name
    #
    # def get_empty_random_block():
    #     x = random.randint(0, COUNT_BLOCKS - 1)
    #     y = random.randint(0, COUNT_BLOCKS - 1)
    #     empty_block = SnakeBlock(x, y)
    #     while empty_block in snake_blocks:
    #         empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
    #         empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
    #     return empty_block
    #
    # x0 = random.randint(0, COUNT_BLOCKS - 5)
    # y0 = random.randint(0, COUNT_BLOCKS - 1)
    #
    # snake_blocks = [SnakeBlock(x0, y0), SnakeBlock(x0 + 1, y0), SnakeBlock(x0 + 2, y0)]  # a head is last
    # apple = get_empty_random_block()
    # d_line = 0
    # d_col = 1
    # speed = 0
    # total = 0
    # records = Records("records1.txt")
    # total_record = records.of_the_player()
    # # all_record_lines = []
    # # r_file_of_records = open("records1.txt", "r")
    # # all_records_lines = r_file_of_records.readlines()
    # # all_to_read = '\n'.join(all_records_lines)
    # # r_file_of_records.close()
    # # if all_to_read.find('/' + name + '/') == -1:
    # #     print('all_to_read', all_to_read)
    # #     total_record = 0
    # #     all_records_lines.append(f'/{total_record}/{name}/\n')
    # # else:
    # #     for lines in all_records_lines:
    # #         if lines.find('/' + name + '/') != -1:
    # #             total_record = int(lines.split('/')[1])
    # #             break
    # # player_records = [total_record, name]
    # while True:
    #     for event in pygame.event.get():  # doing all events
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.KEYDOWN:
    #             if (event.key == pygame.K_w or event.key == pygame.K_UP) and d_col != 0:
    #                 d_line = -1
    #                 d_col = 0
    #             elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and d_col != 0:
    #                 d_line = 1
    #                 d_col = 0
    #             elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and d_line != 0:
    #                 d_line = 0
    #                 d_col = -1
    #             elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and d_line != 0:
    #                 d_line = 0
    #                 d_col = 1
    #
    #     screen.fill(FRAME_WORK)
    #     pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])
    #
    #     text_total = courier.render(f"Total: {total}", False, WHITE)
    #     text_record = courier.render(f"Record: {total_record}", False, WHITE)
    #     screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
    #     screen.blit(text_record, (SIZE_BLOCK + 210, SIZE_BLOCK))
    #     for line in range(COUNT_BLOCKS):
    #         for column in range(COUNT_BLOCKS):
    #             if (line + column) % 2 == 0:
    #                 color = WHITE
    #             else:
    #                 color = BLUE
    #             draw_block(color, column, line)
    #
    #     head = snake_blocks[-1]
    #     if not head.is_inside():
    #         break
    #
    #     draw_block(RED, apple.x, apple.y)
    #     for block in snake_blocks:
    #         draw_block(SNAKE_COLOR, block.x, block.y)
    #     if apple == head:
    #         total += 1
    #         total_record = records.update_of_the_player(total, total_record)
    #         # if total > total_record:
    #         #     flag = True
    #         #     total_record = total
    #         speed = total // 2
    #         snake_blocks.append(apple)
    #         apple = get_empty_random_block()
    #
    #     new_head = SnakeBlock(head.x + d_col, head.y + d_line)
    #     if new_head in snake_blocks:
    #         break
    #     snake_blocks.append(new_head)
    #     snake_blocks.pop(0)
    #
    #     pygame.display.flip()  # we apply everything that we have drawn on the screen
    #     timer.tick(4 + speed)
    #
    # records.update_list_all_players(total_record)
    # # def res_key(line_):
    # #     list_line = line_.split('/')
    # #     print(list_line)
    # #     return int(list_line[1])
    # # if flag:
    # #     lol_flag = 1
    # #
    # #     for lines in range(len(all_records_lines)):
    # #         if all_records_lines[lines].find(name) != -1 and lol_flag != -1:
    # #             all_records_lines[lines] = f'/{total_record}/{name}/\n'
    # #             print('all_record_lines', all_records_lines)
    # #             lol_flag = -1
    # #
    # #     all_records_lines.sort(reverse=True, key=res_key)
    # #     w_file_of_records = open("records1.txt", "w")
    # #     for lines in all_records_lines:
    # #         print(lines)
    # #         w_file_of_records.write(lines)
    # #     w_file_of_records.close()


def file_of_difficult(difficult):
    if difficult == 1:
        return 'records1.txt'
    if difficult == 2:
        return 'records2.txt'
    return 'records3.txt'


def records_of_the_game():
    file_of_records = file_of_difficult(difficulty_of_game)
    r_file_of_records = open(file_of_records, "r")
    all_records = r_file_of_records.readlines()
    flag = True
    while flag:
        for event in pygame.event.get():  # doing all events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                flag = False
        screen.fill(FRAME_WORK)
        screen.blit(arial.render("TOP 10 Players", False, WHITE), (SIZE_BLOCK + 170, SIZE_BLOCK))
        i = 1
        for line_record in all_records:
            text_name_record = line_record.split('/')[2]
            text_total_record = line_record.split('/')[1]
            text_record = arial.render(f"№{i}: {text_name_record} {text_total_record}", False, WHITE)
            i += 1
            screen.blit(text_record, (SIZE_BLOCK, SIZE_BLOCK + 2 * i * SIZE_BLOCK))
            if i == 11:
                break

        pygame.display.flip()
    r_file_of_records.close()


menu = pygame_menu.Menu('Welcome', 400, 400,
                        theme=pygame_menu.themes.THEME_BLUE)


player_name = menu.add.text_input('Name :', default='Player1', onchange=my_text_value, onreturn=my_text_value)
menu.add.button('Records', records_of_the_game)
print(player_name)
menu.add.selector('Level :', [('Easy', 1), ('Medium', 2), ('Hard', 3)],
                  onchange=set_difficulty, onreturn=set_difficulty)
menu.add.selector('Snake Color: ', [('Green', 1), ('Yellow', 2), ('Pink', 3)], onchange=set_color, onreturn=set_color)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
print(name)

while True:

    screen.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()

