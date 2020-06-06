"""
headsup.py

Needed:
Python 3.8 and up

Requirements:
See requirements.txt
"""


import queue
import sys
import subprocess
import threading
import configparser
import logging
from pathlib import Path

import chess


APP_NAME = 'HeadsUp'
APP_VER = 'v1.0.3'
APP_AUTHOR = 'Ferdy'


PIECE_VALUE_SWITCH = 62
MOVE_NUMBER_SWITCH = 0


class ChessAI:
    def __init__(self, engine_file):
        self.engine_file = engine_file
        self.__engine__ = self.__engine_process__()
        self.option = self.engine_options()
        self.engine_name = self.name()

    def __engine_process__(self):
        return subprocess.Popen(self.engine_file, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True, bufsize=1,
                                creationflags=subprocess.CREATE_NO_WINDOW)

    def engine_options(self):
        engine_option = []
        self.send('uci')
        for eline in iter(self.__engine__.stdout.readline, ''):
            line = eline.strip()
            if line.startswith('option name '):
                sp = line.split('option name ')[1]
                name = sp.split('type')[0].strip()
                engine_option.append(name)
            if 'uciok' in line:
                break

        return engine_option

    def name(self):
        idname = None
        self.send('uci')
        for eline in iter(self.__engine__.stdout.readline, ''):
            line = eline.strip()
            if 'id name' in line:
                idname = line.split('id name ')[1]
            if 'uciok' in line:
                break

        return idname

    def author(self):
        idauthor = None
        self.send('uci')
        for eline in iter(self.__engine__.stdout.readline, ''):
            line = eline.strip()
            if 'id author' in line:
                idauthor = line.split('id author ')[1]
            if 'uciok' in line:
                break

        return idauthor

    def uci(self):
        is_show_lines = False
        self.send('uci')
        for eline in iter(self.__engine__.stdout.readline, ''):
            if is_show_lines:
                self.console_print(eline)
            if 'uciok' in eline:
                break

    def ucinewgame(self):
        self.send('ucinewgame')

    def isready(self):
        self.send('isready')
        for eline in iter(self.__engine__.stdout.readline, ''):
            self.console_print(eline)
            if 'readyok' in eline:
                logging.info(f'{self.engine_name} sent readyok')
                break

    def position(self, command):
        self.send(command)

    def stop(self):
        self.send('stop')

        for eline in iter(self.__engine__.stdout.readline, ''):
            self.console_print(eline)
            if 'bestmove ' in eline:
                break

    def ponderhit(self, thr_event):
        self.send('ponderhit')

        for eline in iter(self.__engine__.stdout.readline, ''):
            self.console_print(eline)
            if 'bestmove ' in eline:
                break

    def go(self, command):
        self.send(command)

        for eline in iter(self.__engine__.stdout.readline, ''):
            self.console_print(eline)
            if 'bestmove ' in eline:
                break

    def go_infinite(self, command, thr_event):
        self.send(command)

        while not thr_event.isSet():
            for eline in iter(self.__engine__.stdout.readline, ''):
                if thr_event.wait(0.01):
                    break
                self.console_print(eline)

    def go_ponder(self, command, thr_event):
        self.send(command)

        while not thr_event.is_set():
            for eline in iter(self.__engine__.stdout.readline, ''):
                if thr_event.wait(0.01):
                    break
                self.console_print(eline)

    def console_print(self, msg):
        print(f'{msg.rstrip()}')
        sys.stdout.flush()

    def setoption(self, command):
        self.send(command)

    def quit(self):
        self.send('quit')
        logging.info(f'{self.engine_name} received quit.')

    def send(self, command):
        self.__engine__.stdin.write(f'{command}\n')


def get_config_info(cfg_file):
    """
    Read cfg file and return engine1 and engine2 file paths,
    piece value and move number switches and logging.
    """
    e1, e2, pvs, mns, islog = (None, None, PIECE_VALUE_SWITCH,
                               MOVE_NUMBER_SWITCH, False)

    parser = configparser.ConfigParser()
    parser.read(cfg_file)
    for section_name in parser.sections():
        sname = section_name.lower()
        for name, value in parser.items(section_name):
            if sname == 'engine1':
                if name == 'enginefile':
                    e1 = value
                    print(f'info string set {name} to {value}')
            elif sname == 'engine2':
                if name == 'enginefile':
                    e2 = value
                    print(f'info string set {name} to {value}')
            elif sname == 'headsup option':
                if name == 'piece_value_switch':
                    pvs = int(value)
                    print(f'info string set {name} to {value}')
                elif name == 'move_number_switch':
                    mns = int(value)
                    print(f'info string set {name} to {value}')
                elif name == 'log':
                    islog = True if value.lower() == 'true' else False
                    print(f'info string set {name} to {value.lower()}')

    return e1, e2, pvs, mns, islog


def get_piece_value(board):
    """
    Returns total piece value on the board except kings and pawns.
    Q = 9, R = 5, B = N = 3

    :param board: a python-chess board
    :return: piece values
    """
    epd = board.epd()
    p = epd.split()[0]

    wn = p.count('N')
    wb = p.count('B')
    wr = p.count('R')
    wq = p.count('Q')

    bn = p.count('n')
    bb = p.count('b')
    br = p.count('r')
    bq = p.count('q')

    return 3*(wn+wb+bn+bb) + 5*(wr+br) + 9*(wq+bq)


def get_move_list(pos_line):
    """
    :param pos_line: e.g. position startpos moves e2e4 or
    position [FEN] moves e2e4
    :return: a list of moves
    """
    a = pos_line.split()
    move_index = a.index('moves')
    moves = a[move_index+1:]
    moves = ' '.join(moves)
    moves = moves.strip()

    return moves.split()


def get_fen(pos_line):
    """
    :param pos_line: e.g. position [FEN]
    :return: FEN
    """
    fen = pos_line.rstrip().split()
    fen = fen[2:8]
    fen = ' '.join(fen)
    fen = fen.strip()

    return fen


def engine_loop(engine, name, thr_event, que):
    while True:
        command = que.get()

        if command.startswith('position '):
            engine.position(command)
            logging.info(f'{name} received {command}')

        elif command == 'go infinite':
            engine.go_infinite(command, thr_event)
            logging.info(f'{name} received {command}')

        elif command.startswith('go ponder'):
            engine.go_ponder(command, thr_event)
            logging.info(f'{name} received {command}')

        elif command.startswith('go '):
            engine.go(command)
            logging.info(f'{name} received {command}')

        elif command == 'stop':
            engine.stop()
            logging.info(f'{name} received {command}')

        elif command == 'ponderhit':
            engine.ponderhit(thr_event)
            logging.info(f'{name} received {command}')

        elif command == 'isready':
            engine.isready()
            logging.info(f'{name} received {command}')

        elif 'setoption ' in command:
            engine.setoption(command)
            logging.info(f'{name} received {command}')

        elif command == 'uci':
            engine.uci()
            logging.info(f'{name} received {command}')

        elif command == 'ucinewgame':
            engine.ucinewgame()
            logging.info(f'{name} received {command}')

        elif command == 'quit':
            break


def main():
    print(f'info string {APP_NAME} {APP_VER} a uci engine adapter.')
    cfg_file = 'headsup.cfg'

    # Check headsup.cfg in the same dir with headsup.py or headsup.exe
    config_file = Path(cfg_file)
    if not config_file.is_file():
        print(f'{cfg_file} file is required to run {APP_NAME}! Exiting ...')
        sys.exit(1)

    # Get engine files and switch conditions from config file.
    (engine1_file, engine2_file, piece_value_switch,
     move_number_switch, is_logging) = get_config_info(cfg_file)

    if is_logging:
        logging.basicConfig(
            filename='log_headsup.txt', filemode='w', level=logging.DEBUG,
            format='%(asctime)s :: %(levelname)s :: %(message)s')

    # Check engine files based on headsup.cfg
    if engine1_file is None:
        logging.info('engine1 is missing.')
        sys.exit(1)
    if engine2_file is None:
        logging.info('engine2 is missing.')
        sys.exit(1)

    engine1 = ChessAI(engine1_file)
    name1 = engine1.name()

    engine2 = ChessAI(engine2_file)
    name2 = engine2.name()

    # Set engine options.
    parser = configparser.ConfigParser()
    parser.read(cfg_file)
    for section_name in parser.sections():
        sname = section_name.lower()
        for name, value in parser.items(section_name):
            if sname == 'engine1':
                if name in [opt.lower() for opt in engine1.option]:
                    engine1.setoption(f'setoption name {name} value {value}')
                    print(f'info string setoption name {name} '
                          f'value {value} for {name1}')
            elif sname == 'engine2':
                if name in [opt.lower() for opt in engine2.option]:
                    engine2.setoption(f'setoption name {name} value {value}')
                    print(f'info string setoption name {name} '
                          f'value {value} for {name2}')

    que1 = queue.Queue()
    thr_event1 = threading.Event()
    thr1 = threading.Thread(target=engine_loop, args=(
        engine1, name1, thr_event1, que1), daemon=True)
    thr1.start()

    que2 = queue.Queue()
    thr_event2 = threading.Event()
    thr2 = threading.Thread(target=engine_loop, args=(
        engine2, name2, thr_event2, que2), daemon=True)
    thr2.start()
    is_engine1 = True

    while True:
        command = input('').strip()

        if command == 'uci':
            print(f'id name {APP_NAME} {APP_VER}')
            print(f'id author {APP_AUTHOR}')
            print('option name Ponder type check default false')
            print('option name MultiPV type spin default 1 min 1 max 500')
            print('uciok')

        elif command == 'ucinewgame':
            if is_engine1:
                thr_event1.clear()
                que1.put(command)
            else:
                thr_event2.clear()
                que2.put(command)

        elif command == 'isready':
            if is_engine1:
                thr_event1.clear()
                que1.put(command)
            else:
                thr_event2.clear()
                que2.put(command)

        elif command == 'quit':
            if is_engine1:
                que1.put(command)
            else:
                que2.put(command)
            break

        elif command == 'ponderhit':
            if is_engine1:
                thr_event1.set()
                que1.put(command)
            else:
                thr_event2.set()
                que2.put(command)

        elif command.startswith('position '):
            # Update board to get material and check to switch engine.
            if 'startpos' in command:
                board = chess.Board()

            elif 'fen ' in command:
                fen = get_fen(command)
                board = chess.Board(fen)

            if 'moves' in command:
                move_list = get_move_list(command)
                for m in move_list:
                    board.push(chess.Move.from_uci(m))

            piece_value = get_piece_value(board)
            logging.info(f'piece value: {piece_value}')
            full_move_number = board.fullmove_number
            logging.info(f'full move number: {full_move_number}')
            logging.info(f'playing as {"white" if board.turn else "black"}')

            if (full_move_number < move_number_switch
                    and piece_value > piece_value_switch):
                is_engine1 = True
            else:
                is_engine1 = False

            if is_engine1:
                que1.put(command)
            else:
                que2.put(command)

        elif command == 'go infinite':
            if is_engine1:
                thr_event1.clear()
                que1.put(command)
            else:
                thr_event2.clear()
                que2.put(command)

        elif command.startswith('go ponder'):
            if is_engine1:
                thr_event1.clear()
                que1.put(command)
            else:
                thr_event2.clear()
                que2.put(command)

        elif command.startswith('go '):
            if is_engine1:
                thr_event1.clear()
                que1.put(command)
            else:
                thr_event2.clear()
                que2.put(command)

        elif 'stop' in command:
            if is_engine1:
                thr_event1.set()
                que1.put(command)
            else:
                thr_event2.set()
                que2.put(command)

        elif 'setoption ' in command:
            if is_engine1:
                que1.put(command)
                que2.put(command)
            else:
                que1.put(command)
                que2.put(command)

        else:
            print(f'info string unknown command {command}')
            sys.stdout.flush()

    engine1.quit()
    engine2.quit()


if __name__ == "__main__":
    main()
