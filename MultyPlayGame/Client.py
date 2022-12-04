import socket
import pygame

WIDTH_WINDOW = 1000
HEIGHT_WINDOW = 800
colors = dict(yellow=(255, 255, 0), green=(255, 0, 0), red=(0, 255, 0), violet=(128, 0, 128))
my_name = 'Gleb'
GRID_COLOR = (150, 150, 150)


def reading_datas(s):
    begin = -1
    for i in range(len(s)):
        if s[i] == '<':
            begin = i
        if (s[i] == '>') and (begin != -1):
            end = i
            res = s[begin + 1:end]
            return res
    return ''


def draw_opponents(data_):
    for i in range(len(data_)):
        j = data_[i].split()
        x = WIDTH_WINDOW // 2 + int(j[0])
        y = HEIGHT_WINDOW // 2 + int(j[1])
        r = int(j[2])
        color = colors[j[3]]
        pygame.draw.circle(screen, color, (x, y), r)

        if len(j) == 5:
            write_name(x, y, r, j[4])


def write_name(x, y, r, name):
    font = pygame.font.Font(None, r)
    text = font.render(name, True, (0, 0, 0))
    rect = text.get_rect(center=(x, y))
    screen.blit(text, rect)


class Me:
    def __init__(self, data_):
        data__ = data_.split()
        self.r = int(data__[0])
        self.color = data__[1]

    def update(self, new_radius):
        self.r = new_radius

    def draw(self):
        if self.r != 0:
            pygame.draw.circle(screen, colors[self.color],
                               (WIDTH_WINDOW // 2, HEIGHT_WINDOW // 2),
                               self.r)
            write_name(WIDTH_WINDOW // 2, HEIGHT_WINDOW // 2, self.r, my_name)


class Grid:
    def __init__(self, screen_):
        self.screen = screen_
        self.x = 0
        self.y = 0
        self.start_size = 200
        self.size = self.start_size

    def update(self, real_x, real_y, scale):
        self.size = self.start_size // scale
        self.x = - self.size + (- real_x) % self.size
        self.y = - self.size + (- real_y) % self.size

    def draw(self):
        for i in range(WIDTH_WINDOW // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOR,
                             [self.x + i * self.size, 0],  # coordinates of the highest line
                             [self.x + i * self.size, HEIGHT_WINDOW],
                             1)
        for i in range(HEIGHT_WINDOW // self.size + 2):
            pygame.draw.line(self.screen, GRID_COLOR,
                             [0, self.y + i * self.size],
                             [WIDTH_WINDOW, self.y + i * self.size],
                             1)


# create the window of the game
pygame.init()
screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
pygame.display.set_caption('Slither.IOCopy')

# подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 10000))
# sending to the server our name and sizes of the window
sock.send(('.' + my_name + ' ' + str(WIDTH_WINDOW) + ' ' + str(HEIGHT_WINDOW) + '.').encode())
# getting our radius and color
data = sock.recv(64).decode()
# we confirm what we got
sock.send('!'.encode())
print('Got 1', data)
me = Me(data)
grid = Grid(screen)

running = True
old_v = (0, 0)
v = (-1, -1)
while running:
    # reading command
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # reading state of cursor

    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        v = (pos[0] - WIDTH_WINDOW // 2, pos[1] - HEIGHT_WINDOW // 2)
        if v[0]**2 + v[1]**2 <= me.r**2:
            v = (0, 0)

    # sending the command
    # sending vector if he has been changing
    if v != old_v:
        old_v = v
        message = '<' + str(v[0]) + ',' + str(v[1]) + '>'
        print(message)
        sock.send(message.encode())

    # get from the server new state
    try:
        data = sock.recv(2**20)
    except ConnectionAbortedError:
        running = False
        continue
    data = data.decode()
    print('GOT begin', data)
    data = reading_datas(data)
    print('GOT middle', data)
    data = data.split(',')

    print('Got', data)
    # обработка сообщения сервера
    if data != ['']:
        parameters = list(map(int, data[0].split()))
        # me.update(int(data.pop(0)))
        me.update(parameters[0])
        grid.update(parameters[1], parameters[2], parameters[3])
        # drawing new state
        screen.fill('gray25')
        grid.draw()
        draw_opponents(data[1::])
        # pygame.draw.circle(screen, colors[my_color], (WIDTH_WINDOW // 2, HEIGHT_WINDOW // 2), my_radius)
        me.draw()
    pygame.display.update()
pygame.quit()
