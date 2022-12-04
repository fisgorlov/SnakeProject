import socket
import random
import pygame

FPS = 100
WIDTH_ROOM, HEIGHT_ROOM = 4000, 4000
WIDTH_SERVER_WINDOW, HEIGHT_SERVER_WINDOW = 300, 300
START_PLAYER_SIZE = 50
MICROBES_SIZE = 15
MICROBES_QUANTITY = (WIDTH_ROOM * HEIGHT_ROOM) // 80000
GRID_COLOR = (150, 150, 150)

work_on_server = True
server_ip = 'localhost'

MOBS_QUANTITY = 30
colors = dict(yellow=(255, 255, 0), green=(255, 0, 0), red=(0, 255, 0), violet=(128, 0, 128))
keys_colors = []
for key in colors.keys():
    keys_colors.append(key)


def new_radius(r1_, r_):
    return (r_ ** 2 + r1_ ** 2) ** 0.5


def find(s):
    begin = -1
    for i in range(len(s)):
        if s[i] == '<':
            begin = i
        if (s[i] == '>') and (begin != -1):
            end = i
            res = s[begin + 1:end]
            res = list(map(int, res.split(',')))
            return res
    return ''


class Microbe:
    def __init__(self, x_, y_, r_, color_):
        self.x = x_
        self.y = y_
        self.r = r_
        self.color = color_


class Player:
    def __init__(self, conn_, addr_, x_, y_, r_, color_):
        self.conn = conn_
        self.addr = addr_
        self.x = x_
        self.y = y_
        self.r = r_
        self.color = color_
        self.error = 0
        self.dead = 0
        self.speed_x = 0
        self.speed_y = 0
        self.abs_speed = 100 / (self.r**0.4)
        self.scale = 1
        self.width_window = 1000
        self.height_window = 800
        self.w_vision = 1000
        self.h_vision = 800
        self.ready = False
        self.name = '#Ivan№1'

    def set_options(self, data_):
        data__ = data_[1:-1].split(' ')
        self.name = data__[0]
        self.width_window = int(data__[1])
        self.height_window = int(data__[2])
        self.w_vision = int(data__[1])
        self.h_vision = int(data__[2])

        print(self.name, self.width_window, self.height_window)

    def update(self):
        # x coordinates
        if self.x - self.r <= 0:
            if self.speed_x >= 0:
                self.x += self.speed_x
        else:
            if self.x + self.r >= WIDTH_ROOM:
                if self.speed_x <= 0:
                    self.x += self.speed_x
            else:
                self.x += self.speed_x
        # y coordinates
        if self.y - self.r <= 0:
            if self.speed_y >= 0:
                self.y += self.speed_y
        else:
            if self.y + self.r >= WIDTH_ROOM:
                if self.speed_y <= 0:
                    self.y += self.speed_y
            else:
                self.y += self.speed_y
        if self.r != 0:
            self.abs_speed = 30 / (self.r ** 0.5)
        else:
            self.abs_speed = 0

        # change radius
        if self.r >= 100:
            self.r = self.r - self.r / 10000

        # change the scale
        if (self.r >= self.w_vision / 4) or (self.r >= self.h_vision / 4):
            if (self.w_vision <= WIDTH_ROOM) or (self.h_vision <= HEIGHT_ROOM):
                self.scale *= 2
                self.w_vision = self.width_window * self.scale
                self.h_vision = self.height_window * self.scale
        if (self.r < self.w_vision / 8) and (self.r < self.h_vision / 8):
            if self.scale > 1:
                self.scale //= 2
                self.w_vision = self.width_window * self.scale
                self.h_vision = self.height_window * self.scale

    def change_speed(self, v):
        if (v[0] == 0) and (v[1] == 0):
            self.speed_x = 0
            self.speed_y = 0
        else:
            len_v = (v[0]**2 + v[1]**2)**0.5
            v = (v[0] / len_v, v[1] / len_v)
            v = (v[0] * self.abs_speed, v[1] * self.abs_speed)
            self.speed_x, self.speed_y = v[0], v[1]


# creating the sockets
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind((server_ip, 10000))  # связались с портом компа
main_socket.setblocking(False)
main_socket.listen(5)

# creating start window
pygame.init()
if not work_on_server:
    screen = pygame.display.set_mode((WIDTH_SERVER_WINDOW, HEIGHT_SERVER_WINDOW))
clock = pygame.time.Clock()

# creating the starter kit of mobs
players = [Player(None, None,
                  random.randint(0, WIDTH_ROOM),
                  random.randint(0, HEIGHT_ROOM),
                  random.randint(10, 100),
                  random.choice(keys_colors))
           for i in range(MOBS_QUANTITY)]

# creating the starter kit of MICROBES
microbes = [Microbe(random.randint(0, WIDTH_ROOM),
                    random.randint(0, HEIGHT_ROOM),
                    MICROBES_SIZE,
                    random.choice(keys_colors))
            for i in range(MICROBES_QUANTITY)]
tick = -1
server_works = True
while server_works:
    tick += 1
    clock.tick(FPS)
    if tick == 200:
        tick = 0
        # проверим есть ли желающие войти в игру
        try:
            new_socket, addr = main_socket.accept()
            print('Подключился', addr)
            new_socket.setblocking(False)
            spawn = random.choice(microbes)
            new_player = Player(new_socket, addr, spawn.x,
                                spawn.y,
                                START_PLAYER_SIZE,
                                random.choice(keys_colors))
            microbes.remove(spawn)
            # message = str(new_player.r) + ' ' + new_player.color
            # new_player.conn.send(message.encode())
            players.append(new_player)
        except:
            print('Nobody people')
        # complementing list of mods
        for i in range(MOBS_QUANTITY - len(players)):
            if len(microbes) != 0:
                spawn = random.choice(microbes)
                players.append(Player(None, None,
                                      spawn.x,
                                      spawn.y,
                                      random.randint(10, 100),
                                      random.choice(keys_colors)))
                microbes.remove(spawn)
        # complementing list of microbes
        new_microbes = [Microbe(random.randint(0, WIDTH_ROOM),
                        random.randint(0, HEIGHT_ROOM),
                        MICROBES_SIZE,
                        random.choice(keys_colors))
                        for i in range(MICROBES_QUANTITY - len(microbes))]
        microbes += new_microbes
    # reading player's commands
    for player in players:
        if player.conn is not None:
            try:
                data = player.conn.recv(1024)
                data = data.decode()
                if data[0] == '!':  # we got a message about player readiness
                    player.ready = True
                else:
                    if data[0] == '.' and data[-1] == '.':  # we got a name and a size of the player's window
                        player.set_options(data)
                        player.conn.send((str(START_PLAYER_SIZE) + ' ' + player.color).encode())
                    else:  # got a vector from cursor
                        data = find(data)
                        print('Got', data)
                        player.change_speed(data)
            except:
                pass
        else:
            if tick == 100:
                data = [random.randint(-100, 100), random.randint(-100, 100)]
                player.change_speed(data)
        player.update()

    # what is the player seeing
    visible_balls = [[] for i in range(len(players))]
    for i in range(len(players)):
        # what microbes is seeing i-th player
        for k in range(len(microbes)):
            dist_x = microbes[k].x - players[i].x
            dist_y = microbes[k].y - players[i].y
            # i is seeing k
            if (
                    (abs(dist_x) <= (players[i].w_vision // 2 + microbes[k].r))
                    and
                    (abs(dist_y) <= (players[i].h_vision // 2 + microbes[k].r))
                    ):
                # i can eat k
                if (dist_x**2 + dist_y**2)**0.5 <= players[i].r:
                    players[i].r = new_radius(players[i].r, microbes[k].r)
                    microbes[k].r = 0
                if (players[i].conn is not None) and (microbes[k].r != 0):
                    # prepare datas to appending into visible balls
                    x_send = str(round(dist_x / players[i].scale))
                    y_send = str(round(dist_y / players[i].scale))
                    r_send = str(round(microbes[k].r / players[i].scale))
                    col_send = microbes[k].color

                    visible_balls[i].append(x_send + ' ' + y_send + ' ' + r_send + ' ' + col_send)
        for j in range(i + 1, len(players)):
            # we consider a pair of the i-th and j-th player
            dist_x = players[i].x - players[j].x
            dist_y = players[i].y - players[j].y

            # i see j
            if (
                    (abs(dist_x) <= (players[i].w_vision // 2 + players[j].r))
                    and
                    (abs(dist_y) <= (players[i].h_vision // 2 + players[j].r))
                    ):
                # i can eat j
                if ((dist_x**2 + dist_y**2)**0.5 <= players[i].r) and (players[i].r > 1.05 * players[j].r):
                    # # # # change radius
                    players[i].r = new_radius(players[i].r, players[j].r)
                    players[j].r, players[j].speed_x, players[j].speed_y = 0, 0, 0
                if players[i].conn is not None:

                    # prepare datas to append into the list showing 3D circles
                    x_send = str(round(-dist_x / players[i].scale))
                    y_send = str(round(-dist_y / players[i].scale))
                    r_send = str(round(players[j].r / players[i].scale))
                    color_send = players[j].color
                    name_send = players[j].name
                    if players[j].r >= 30 * players[i].scale:
                        visible_balls[i].append(x_send + ' ' + y_send + ' ' + r_send
                                                + ' ' + color_send + ' ' + name_send)
                    else:
                        visible_balls[i].append(x_send + ' ' + y_send + ' ' + r_send + ' ' + color_send)

            #j see i
            if (
                    (abs(dist_x) <= players[j].w_vision // 2 + players[i].r)
                    and
                    (abs(dist_y) <= players[j].h_vision // 2 + players[i].r)
            ):
                # j can eat i

                if ((dist_x**2 + dist_y**2)**0.5 <= players[j].r) and (players[j].r > 1.05 * players[i].r):
                    # # # # change radius
                    players[j].r = new_radius(players[j].r, players[i].r)
                    players[i].r, players[i].speed_x, players[i].speed_y = 0, 0, 0
                if players[j] is not None:
                    x_send = str(round(dist_x / players[j].scale))
                    y_send = str(round(dist_y / players[j].scale))
                    r_send = str(round(players[i].r / players[j].scale))
                    color_send = players[i].color
                    name_send = players[i].name

                    if players[i].r >= 30 * players[j].scale:
                        visible_balls[j].append(x_send + ' ' + y_send + ' ' + r_send
                                                + ' ' + color_send + ' ' + name_send)
                    else:
                        visible_balls[j].append(x_send + ' ' + y_send + ' ' + r_send + ' ' + color_send)

    # doing  the answer for each player
    answers = ['' for i in range(len(players))]
    for i in range(len(players)):
        r_send = str(round(players[i].r / players[i].scale))
        x_send = str(round(players[i].x / players[i].scale))
        y_send = str(round(players[i].y / players[i].scale))
        scale_send = str(players[i].scale)
        visible_balls[i] = [r_send + ' ' + x_send + ' ' + y_send + ' ' + scale_send] + visible_balls[i]
        answers[i] = '<' + (','.join(visible_balls[i])) + '>'
    # reading commands of the player
    # sending new state of playing field
    for i in range(len(players)):
        if (players[i].conn is not None) and players[i].ready:
            try:
                players[i].conn.send(answers[i].encode())
                players[i].error = 0
            except:
                players[i].error += 1
    # cleaning the list from disconnected players
    for player in players:
        if player.r == 0:
            if player.conn is not None:
                player.dead += 1
            else:
                player.dead += 300

        if (player.error == 50) or (player.dead == 300):
            if player.conn is not None:
                player.conn.close()
            players.remove(player)
    # cleaning the list from eaten microbes
    for microbe in microbes:
        if microbe.r == 0:
            microbes.remove(microbe)
    if not work_on_server:
        # drawing the state of the room
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                server_works = False

        screen.fill('BLACK')
        for player in players:
            x = round(player.x * WIDTH_SERVER_WINDOW / WIDTH_ROOM)
            y = round(player.y * HEIGHT_SERVER_WINDOW / HEIGHT_ROOM)
            r = round(player.r * WIDTH_SERVER_WINDOW / WIDTH_ROOM)
            col = colors[player.color]
            pygame.draw.circle(screen, col, (x, y), r)
        pygame.display.update()


pygame.quit()
main_socket.close()
