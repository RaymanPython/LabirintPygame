import tkinter
import pygame
from pygame.locals import *
import PIL
from PIL import Image
from PIL import ImageDraw
import random
import os
from tkinter import *


class Stak:
    def __init__(self, *a):
        self.a = list(a)


    def push(self, n):
        self.a = [n] + self.a
        return self.a


    def pop(self):
        if len(self.a) > 0:
            res = self.a[-1]
            self.a = self.a[:-1]
            return res
        else:
            print('error')


    def back(self):
        if len(self.a) > 0:
            return self.a[-1]
        else:
            print('error')

    def __len__(self):
        return len(self.a)

    def clear(self):
        self.a = []
        return self.a


def fin(b, value):
    c = False
    for i in b:
        if value in i:
            c = True
            break
    return c



class Grafh:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grafh = [[[1, 1, 1, 1] for i in range(m)] for j in range(n)]
        b = [[True for i in range(m)] for j in range(n)]
        x, y = 0, 0
        b[x][y] = False
        c = True
        a = Stak()
        while fin(b, True) and c:
            c = False
            sx = x
            sy = y
            r = self.grafh[sx][sy]
            if b[sx][sy]:
                b[sx][sy] = False
            ran = []
            if r[0] == 1:
                if 0 <= sx and sx < n and 0 < sy - 1 and sy - 1 < m:
                    if b[sx][sy - 1]:
                        ran.append(0)
            if r[1] == 1:
                if 0 <= sx + 1 and sx + 1 < n and 0 <= sy and sy < m:
                    if b[sx + 1][sy]:
                        ran.append(1)
            if r[2] == 1:
                if 0 <= sx and sx < n and 0 < sy + 1 and sy + 1 < m:
                    if b[sx][sy + 1]:
                        ran.append(2)
            if r[3] == 1:
                if 0 <= sx - 1 and sx - 1 < n and 0 < sy and sy < m:
                    if b[sx - 1][sy]:
                        ran.append(3)
            if len(ran) > 0:
                s = random.choice(ran)
                # s = ran[-1]
                if s == 0:
                    y = sy - 1
                    c = True
                    self.grafh[sx][sy][0] = 0
                    self.grafh[sx][sy - 1][2] = 0
                elif s == 1:
                    x = sx + 1
                    c = True
                    self.grafh[sx][sy][1] = 0
                    self.grafh[sx + 1][sy][3] = 0
                elif s == 2:
                    y = y + 1
                    c = True
                    self.grafh[sx][sy][2] = 0
                    self.grafh[sx][sy + 1][0] = 0
                elif s == 3:
                    x = x - 1
                    c = True
                    self.grafh[sx][sy][3] = 0
                    self.grafh[sx - 1][sy][1] = 0
                a.push([x, y])
                b[x][y] = False
            elif len(a) > 0:
                c = True
                r = a.back()
                x, y = r[0], r[1]
                a.pop()
            else:
                rand = []
                for i in range(len(b)):
                    for j in range(len(b[0])):
                        if b[i][j]:
                            rand.append([i, j])
                if len(rand) > 0:
                    rand = random.choice(rand)
                    x, y = rand[0], rand[1]
                    b[x][y] = False
                    c = True
                    a.push([x, y])
                else:
                    c = False
                    break

    def dfs(self, x, y, x1, y1):
        self.dfs = []
        c = True
        a = [[x, y]]
        k = 0
        b = [[-1 for i in range(self.m)] for j in range(self.n)]
        b[x][y] = 0
        color = 1
        while c:
            c = False
            k1 = len(a)
            for i in range(k, len(a)):
                sx = a[i][0]
                sy = a[i][1]
                s = self.grafh[sx][sy]
                if s[0] == 0:
                    if b[sx][sy - 1] == -1:
                        c = True
                        a.append([sx, sy - 1])
                        b[sx][sy - 1] = color
                if s[1] == 0:
                    if b[sx + 1][sy] == -1:
                        c = True
                        a.append([sx + 1, sy])
                        b[sx + 1][sy] = color
                if s[2] == 0:
                    if b[sx][sy + 1] == -1:
                        c = True
                        a.append([sx, sy + 1])
                        b[sx][sy + 1] = color
                if s[3] == 0:
                    if b[sx - 1][sy] == -1:
                        c = True
                        a.append([sx - 1, sy])
                        b[sx - 1][sy] = color
            color += 1
            k = k1
        while b[x1][y1] != 0:
            s = self.grafh[x1][y1]
            for i in range(4):
                if s[i] == 0:
                    if i == 0:
                        if b[x1][y1 - 1] == b[x1][y1] - 1:
                            x, y = x1, y1 - 1
                            break
                    elif i == 1:
                        if b[x1 + 1][y1] == b[x1][y1] - 1:
                            x, y = x1 + 1, y1
                            break
                    elif i == 2:
                        if b[x1][y1 + 1] == b[x1][y1] - 1:
                            x, y = x1, y1 + 1
                            break
                    elif i == 3:
                        if b[x1 - 1][y1] == b[x1][y1] - 1:
                            x, y = x1 - 1, y1
                            break
            self.dfs.append([(x1, y1), (x, y)])
            x1, y1 = x, y
        return self.dfs


    def dfsdraw(self, screen, size, sx, sy):
        for i in list(self.dfs):
            pygame.draw.line(screen, (0, 0, 255), (i[0][0] * size + size//2 + sx, i[0][1] * size + size//2 + sy), (i[1][0] * size + size//2 + sx, i[1][1] * size + size//2 + sy))

    def pildraw(self, level, size, linesize=10):
        self.level = level
        self.size = size
        im = Image.new("RGB", (self.n * size, self.m * size), (0, 255, 0))
        draw = ImageDraw.Draw(im)
        for i in range(self.n):
            for j in range(self.m):
                a = self.grafh[i][j]
                s = size // 2
                x = i * size + size // 2
                y = j * size + size // 2
                if a[0] == 1:
                    draw.line((x - s, y - s, x + s, y - s), fill='pink', width=linesize)
                if a[1] == 1:
                    draw.line((x + s, y - s, x + s, y + s), fill='pink', width=linesize)
                if a[2] == 1:
                    draw.line((x - s, y + s, x + s, y + s), fill='pink', width=linesize)
                if a[3] == 1:
                    draw.line((x - s, y - s, x - s, y + s), fill='pink', width=linesize)
        im.show()
        im.save(level)

    def __call__(self, screen, size, xs, ys, Color_line=(255, 0, 0)):
        for i in range(self.n):
            for j in range(self.m):
                a = self.grafh[i][j]
                s = size // 2
                x = i * size + size // 2
                x += xs
                y = j * size + size // 2
                y += ys
                if a[0] == 1:
                    pygame.draw.line(screen, Color_line, (x - s, y - s), (x + s, y - s))
                if a[1] == 1:
                    pygame.draw.line(screen, Color_line, (x + s, y - s), (x + s, y + s))
                if a[2] == 1:
                    pygame.draw.line(screen, Color_line, (x - s, y + s), (x + s, y + s))
                if a[3] == 1:
                    pygame.draw.line(screen, Color_line, (x - s, y - s), (x - s, y + s))

    def cor(self, x, y, i):
        return self.grafh[x][y][i] == 0


class Player(pygame.sprite.Sprite):
    def __init__(self, size, x, y, flag):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        if flag:
            self.image = pygame.image.load('worker.png').convert_alpha()
            self.image =  pygame.transform.scale(self.image, (size, size))
        else:
            self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Buttonpygame(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5 * size, size))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.size = size

    def cor(self, x, y):
        return abs(self.rect.center[0] - x) <= 5 * self.size // 2 and abs(self.rect.center[1] - y) <= self.size // 2

    def update(self, x, y):
        return


class Buttonans(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5 * size, size))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.size = size

    def cor(self, x, y):
        return abs(self.rect.center[0] - x) <= 5 * self.size // 2 and abs(self.rect.center[1] - y) <= self.size // 2

    def update(self, x, y):
        return


class Finish(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.size = size


    def update(self, x, y):
        return


def randomcor(n, m):
    x = random.randint(0, n - 1)
    if x == 0:
        y = 0
    else:
        y = random.randint(1,  m - 1)
    return x, y

def main(n, m):
    pygame.init()
    size = 500 // (max(n, m))
    xs = 5
    ys = 50
    sizes = (n * size + xs + 10, m * size + ys + 10)
    screen = pygame.display.set_mode(sizes)
    pygame.display.set_caption('Головоломка лабиринт')
    color = (255, 255, 255)
    a = Grafh(n, m)
    a(screen, size, xs, ys)
    xst, yst = randomcor(n, m)
    xans, yans = randomcor(n, m)
    dfslist = a.dfs(xst, yst, xans, yans)
    x, y = xst, yst
    all_sprites = pygame.sprite.Group()
    player = Player(size - 10, xs + xst * size +  size // 2, ys  + yst * size + size // 2, size >= 30)
    all_sprites.add(player)
    button = Buttonpygame(ys, ys - 10, 5)
    buttonans = Buttonans(ys, size * n - ys, xs)
    all_sprites.add(button)
    all_sprites.add(buttonans)
    finish = Finish(size - 2, xs + xans * size + size // 2, ys + yans * size + size // 2)
    all_sprites.add(finish)
    score = 0
    ans = False
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('Генерировать', True, (0, 0, 255), (0, 255, 0))
    textRect = text.get_rect()
    textRect.center = (ys * 1.5, ys // 3)
    textans = font.render('Ответ', True, (0, 0, 255), (0, 255, 0))
    textRectans = text.get_rect()
    textRectans.center = (size * n - ys * 1.5, ys // 3)
    while True:
        dx = 0
        dy = 0
        if x == xans and y == yans:
            print('Вы ппришли в нужную точку!!!!!!', 'за', score, 'их', len(dfslist))
            pygame.quit()
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                score += 1
                if event.key == pygame.K_LEFT:
                    if a.cor(x, y, 3):
                        x -= 1
                        dx = -size
                        dy = 0
                        # print(x, y)
                elif event.key == pygame.K_RIGHT:
                    if a.cor(x, y, 1):
                        x += 1
                        dx = size
                        dy = 0
                        # print(x, y)
                if event.key == pygame.K_DOWN:
                    if a.cor(x, y, 2):
                        y += 1
                        dx = 0
                        dy = size
                        # print(x, y)
                elif event.key == pygame.K_UP:
                    if a.cor(x, y, 0):
                        y -= 1
                        dx = 0
                        dy = -size
                        # print(x, y)
                else:
                    score -= 1
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button.cor(mouse_x, mouse_y):
                    pygame.quit()
                    break
                if buttonans.cor(mouse_x, mouse_y):
                    ans = True

        screen.fill((0, 0, 0))
        all_sprites.update(dx, dy)
        a(screen, size, xs, ys)
        if ans:
            a.dfsdraw(screen, size, xs, ys)
        all_sprites.draw(screen)
        screen.blit(text, textRect)
        screen.blit(textans, textRectans)
        pygame.display.update()
    return True

def click():
    global txt, booling
    k = txt.get()
    try:
        n, m = map(int, k.split())
        window.mainloop()
        while True:
            try:
                if main(n, m):
                    continue
                else:
                    break
            except:
                continue
    except:
        print('Некорктный ввод!')


def turn():
    global txt, booling
    global window
    window = Tk()
    window.title("Добро пожаловать в приложение Лабиринт")
    window.geometry('650x400')
    window.wm_attributes('-topmost', 1)
    window["bg"] = "#FFF000FFF"
    lbl = []
    lbl1 = (Label(window, text='Введите размера лабиринта, пожалуйста.'))
    lbl1.grid(column=0, row=1)
    txt = Entry(window, width=10)
    txt.grid(column=1, row=1)
    btn = Button(window, text="нажимите сюда!", command=click)
    btn.grid(column=2, row=1)
    window.mainloop()

turn()
#n, m = map(int, input().split())
#main(n, m)

