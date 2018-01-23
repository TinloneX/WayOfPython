#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 此代码应通过命令行执行
# 代码未完善及验证
import curses  # windows 自行下载非官方包
from collections import defaultdict
from random import randrange, choice

ACTIONS = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
KEY_CODE = [ord(ch) for ch in 'WASDRQwasdrq']
ACTION_DICT = dict(zip(KEY_CODE, ACTIONS * 2))


def transpose(field):
    return [list(row) for row in zip(*field)]


def invert(field):
    return [row[::-1] for row in field]


class GameField():
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_score = win
        self.score = 0
        self.highscore = 0
        self.reset()

    def spawn(self):
        """产生新的数字"""
        new_element = 4 if randrange(100) > 89 else 2
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def reset(self):
        """初始化数字"""
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    def move_is_possible(self, direction):
        """判断是否可以移动"""

        def row_is_left_movable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:
                    return True
                return False

            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left'] = lambda field: any(row_is_left_movable(row) for row in field)

        check['Right'] = lambda field: check['Left'](invert(field))

        check['Up'] = lambda field: check['Left'](transpose(field))

        check['Down'] = lambda field: check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

    def move(self, direction):
        """处理移动逻辑"""

        def move_row_left(row):
            def tighten(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + i < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row

            return tighten(merge(tighten(row)))

        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field == moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):
        return any(any(i >= self.win_score for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in ACTIONS)

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'

        def cast(string):
            screen.addstr(string + '\n')

        # 绘制水平分割线
        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()

        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HIGHSCORE: ' + str(self.highscore))

        for row in self.field:
            draw_hor_separator()
            draw_row(row)

        draw_hor_separator()

        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)


def main(stdscr):
    def init():
        """重置游戏棋盘"""
        game_field.reset()
        return 'Game'

    def not_game(state):
        """非游戏进行时的界面"""
        game_field.draw(stdscr)
        action = get_action(stdscr)
        response = defaultdict(lambda: state)
        response['Restart'], response['Exit'] = 'Init', 'Exit'
        return response[action]

    def game():
        """游戏进行时的界面"""
        # 读取用户输入得到的action
        game_field.draw(stdscr)
        action = get_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):  # move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    def get_action(keyboard):
        char = 'N'
        while char not in ACTION_DICT:
            char = keyboard.getch()
        return ACTION_DICT[char]

    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
    }
    curses.use_default_colors()
    game_field = GameField(win=2048)
    state = 'Init'
    while state != 'Exit':
        state = state_actions[state]()


curses.wrapper(main)
